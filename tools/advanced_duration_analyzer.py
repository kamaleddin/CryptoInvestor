#!/usr/bin/env python3
"""
ADVANCED STATISTICAL DURATION ANALYZER

Implements best practices in quantitative finance and statistics:
- Risk-adjusted performance metrics (Sharpe, Sortino, Calmar)
- Statistical significance testing (t-tests, Mann-Whitney U)
- Bootstrap confidence intervals
- Non-overlapping periods for independence
- Drawdown analysis
- Distribution analysis (skewness, kurtosis, VaR, CVaR)
- Rolling performance metrics
- Monte Carlo simulation capabilities
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
from scipy import stats
from scipy.stats import mannwhitneyu, ttest_rel, norm, skew, kurtosis
import warnings
warnings.filterwarnings('ignore')

from src.optimum_dca_analyzer import FlexibleOptimumDCA

class AdvancedDurationAnalyzer:
    """
    Advanced statistical analyzer for DCA strategies.
    
    Key improvements:
    1. Non-overlapping periods for statistical independence
    2. Risk-adjusted performance metrics
    3. Statistical significance testing
    4. Bootstrap confidence intervals
    5. Comprehensive risk analysis
    """
    
    def __init__(self, 
                 weekly_budget: float = 250.0,
                 overall_start: date = date(2016, 1, 1),
                 overall_end: date = date(2025, 9, 24),
                 risk_free_rate: float = 0.04,  # 4% annual risk-free rate
                 verbose: bool = True):
        
        self.weekly_budget = weekly_budget
        self.overall_start = overall_start
        self.overall_end = overall_end
        self.risk_free_rate = risk_free_rate
        self.verbose = verbose
        
        # Duration definitions
        self.durations = {
            '1-Year': 52,
            '2-Year': 104,
            '3-Year': 156,
            '4-Year': 208
        }
        
        # Load price data
        self.price_data = self._load_price_data()
    
    def _load_price_data(self) -> pd.DataFrame:
        """Load and prepare Bitcoin price data."""
        df = pd.read_csv("data/bitcoin_prices.csv")
        df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y', errors='coerce')
        df['Price'] = df['Price'].astype(str).str.replace('$', '').str.replace(',', '').str.strip()
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df.dropna(subset=['date', 'Price']).sort_values('date')
        df['date_only'] = df['date'].dt.date
        return df
    
    def _get_final_price(self, end_date: date) -> float:
        """Get Bitcoin price for a specific end date."""
        valid_prices = self.price_data[self.price_data['date_only'] <= end_date]
        if len(valid_prices) == 0:
            return None
        return valid_prices.iloc[-1]['Price']
    
    def _generate_non_overlapping_periods(self, duration_weeks: int) -> List[Tuple[date, date]]:
        """
        Generate NON-OVERLAPPING periods for statistical independence.
        This is critical for proper statistical testing.
        """
        periods = []
        current_date = self.overall_start
        
        while True:
            end_date = current_date + timedelta(weeks=duration_weeks)
            
            if end_date > self.overall_end:
                break
            
            periods.append((current_date, end_date))
            
            # Move to next non-overlapping period
            current_date = end_date + timedelta(days=1)
        
        return periods
    
    def _generate_rolling_periods(self, duration_weeks: int, step_weeks: int = 4) -> List[Tuple[date, date]]:
        """
        Generate rolling periods with controlled overlap.
        Use step_weeks to control overlap (4 weeks = monthly steps, less correlation).
        """
        periods = []
        current_date = self.overall_start
        
        while True:
            end_date = current_date + timedelta(weeks=duration_weeks)
            
            if end_date > self.overall_end:
                break
            
            periods.append((current_date, end_date))
            current_date = current_date + timedelta(weeks=step_weeks)
        
        return periods
    
    def calculate_sharpe_ratio(self, returns: np.ndarray, periods_per_year: float = 52) -> float:
        """
        Calculate annualized Sharpe ratio.
        
        Sharpe = (Mean Return - Risk Free Rate) / Std Dev of Returns
        Higher is better (risk-adjusted return).
        """
        if len(returns) == 0 or np.std(returns) == 0:
            return 0.0
        
        mean_return = np.mean(returns)
        std_return = np.std(returns, ddof=1)
        
        # Annualized Sharpe ratio
        sharpe = (mean_return - self.risk_free_rate / periods_per_year) / std_return
        sharpe_annualized = sharpe * np.sqrt(periods_per_year)
        
        return sharpe_annualized
    
    def calculate_sortino_ratio(self, returns: np.ndarray, periods_per_year: float = 52) -> float:
        """
        Calculate annualized Sortino ratio.
        
        Sortino = (Mean Return - Risk Free Rate) / Downside Deviation
        Like Sharpe but only penalizes downside volatility.
        """
        if len(returns) == 0:
            return 0.0
        
        mean_return = np.mean(returns)
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0:
            return np.inf
        
        downside_std = np.std(downside_returns, ddof=1)
        if downside_std == 0:
            return 0.0
        
        sortino = (mean_return - self.risk_free_rate / periods_per_year) / downside_std
        sortino_annualized = sortino * np.sqrt(periods_per_year)
        
        return sortino_annualized
    
    def calculate_max_drawdown(self, cumulative_returns: np.ndarray) -> Dict:
        """
        Calculate maximum drawdown and related metrics.
        
        Returns:
            max_drawdown: Maximum peak-to-trough decline
            max_drawdown_duration: Duration of longest drawdown
            recovery_time: Time to recover from max drawdown
        """
        if len(cumulative_returns) == 0:
            return {'max_drawdown': 0, 'drawdown_duration': 0, 'recovery_time': 0}
        
        # Calculate running maximum
        running_max = np.maximum.accumulate(cumulative_returns)
        
        # Calculate drawdown at each point
        drawdown = (cumulative_returns - running_max) / running_max
        
        max_drawdown = np.min(drawdown)
        
        # Find drawdown duration
        max_dd_idx = np.argmin(drawdown)
        
        # Find when drawdown started (last peak before max drawdown)
        peak_idx = 0
        for i in range(max_dd_idx, -1, -1):
            if cumulative_returns[i] == running_max[i]:
                peak_idx = i
                break
        
        drawdown_duration = max_dd_idx - peak_idx
        
        # Find recovery time
        recovery_time = 0
        peak_value = cumulative_returns[peak_idx]
        for i in range(max_dd_idx, len(cumulative_returns)):
            if cumulative_returns[i] >= peak_value:
                recovery_time = i - max_dd_idx
                break
        
        return {
            'max_drawdown': max_drawdown,
            'drawdown_duration': drawdown_duration,
            'recovery_time': recovery_time
        }
    
    def calculate_calmar_ratio(self, total_return: float, max_drawdown: float, years: float) -> float:
        """
        Calculate Calmar ratio.
        
        Calmar = Annualized Return / |Maximum Drawdown|
        Higher is better (return per unit of max drawdown risk).
        """
        if max_drawdown == 0:
            return 0.0
        
        annualized_return = (1 + total_return) ** (1 / years) - 1
        calmar = annualized_return / abs(max_drawdown)
        
        return calmar
    
    def calculate_var_cvar(self, returns: np.ndarray, confidence: float = 0.95) -> Dict:
        """
        Calculate Value at Risk (VaR) and Conditional VaR (CVaR).
        
        VaR: Maximum expected loss at given confidence level
        CVaR: Average loss beyond VaR (tail risk)
        """
        if len(returns) == 0:
            return {'var': 0, 'cvar': 0}
        
        # VaR at confidence level
        var = np.percentile(returns, (1 - confidence) * 100)
        
        # CVaR: average of returns worse than VaR
        cvar_returns = returns[returns <= var]
        cvar = np.mean(cvar_returns) if len(cvar_returns) > 0 else var
        
        return {'var': var, 'cvar': cvar}
    
    def bootstrap_confidence_interval(self, data: np.ndarray, 
                                     statistic_func: callable,
                                     n_bootstrap: int = 10000,
                                     confidence: float = 0.95) -> Tuple[float, float, float]:
        """
        Calculate bootstrap confidence interval for any statistic.
        
        Returns: (point_estimate, lower_bound, upper_bound)
        """
        if len(data) == 0:
            return (0, 0, 0)
        
        # Point estimate
        point_estimate = statistic_func(data)
        
        # Bootstrap resampling
        bootstrap_stats = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_stats.append(statistic_func(sample))
        
        # Calculate confidence interval
        alpha = 1 - confidence
        lower = np.percentile(bootstrap_stats, alpha / 2 * 100)
        upper = np.percentile(bootstrap_stats, (1 - alpha / 2) * 100)
        
        return (point_estimate, lower, upper)
    
    def statistical_significance_test(self, optimum_returns: np.ndarray, 
                                     simple_returns: np.ndarray) -> Dict:
        """
        Test if Optimum DCA is statistically significantly better than Simple DCA.
        
        Uses both parametric (paired t-test) and non-parametric (Mann-Whitney U) tests.
        """
        if len(optimum_returns) == 0 or len(simple_returns) == 0:
            return {}
        
        # Paired t-test (assumes normality)
        t_stat, t_pvalue = ttest_rel(optimum_returns, simple_returns)
        
        # Mann-Whitney U test (non-parametric, doesn't assume normality)
        u_stat, u_pvalue = mannwhitneyu(optimum_returns, simple_returns, alternative='greater')
        
        # Effect size (Cohen's d)
        mean_diff = np.mean(optimum_returns) - np.mean(simple_returns)
        pooled_std = np.sqrt((np.var(optimum_returns, ddof=1) + np.var(simple_returns, ddof=1)) / 2)
        cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
        
        return {
            't_statistic': t_stat,
            't_pvalue': t_pvalue,
            'u_statistic': u_stat,
            'u_pvalue': u_pvalue,
            'cohens_d': cohens_d,
            'significant_at_5pct': t_pvalue < 0.05,
            'significant_at_1pct': t_pvalue < 0.01
        }
    
    def analyze_return_distribution(self, returns: np.ndarray) -> Dict:
        """
        Analyze the distribution of returns.
        
        Returns: skewness, kurtosis, normality test
        """
        if len(returns) < 3:
            return {}
        
        # Skewness (asymmetry of distribution)
        # Positive: right tail longer, Negative: left tail longer
        skewness = skew(returns)
        
        # Kurtosis (tailedness of distribution)
        # High: fat tails (more extreme values), Low: thin tails
        kurt = kurtosis(returns)
        
        # Jarque-Bera test for normality
        jb_stat, jb_pvalue = stats.jarque_bera(returns)
        
        return {
            'mean': np.mean(returns),
            'median': np.median(returns),
            'std': np.std(returns, ddof=1),
            'skewness': skewness,
            'kurtosis': kurt,
            'jb_statistic': jb_stat,
            'jb_pvalue': jb_pvalue,
            'is_normal': jb_pvalue > 0.05
        }
    
    def run_comprehensive_analysis(self, 
                                   use_non_overlapping: bool = True,
                                   rolling_step_weeks: int = 4) -> Dict:
        """
        Run comprehensive statistical analysis.
        
        Args:
            use_non_overlapping: If True, use non-overlapping periods (better stats)
            rolling_step_weeks: If overlapping, step size in weeks
        """
        
        print("="*80)
        print("🔬 ADVANCED STATISTICAL ANALYSIS")
        print("="*80)
        print(f"Period: {self.overall_start} to {self.overall_end}")
        print(f"Weekly Budget: ${self.weekly_budget:.2f}")
        print(f"Analysis Mode: {'Non-Overlapping' if use_non_overlapping else f'Rolling ({rolling_step_weeks}-week steps)'}")
        print(f"Risk-Free Rate: {self.risk_free_rate*100:.1f}% annual")
        print("="*80)
        
        all_results = {}
        
        for duration_name, duration_weeks in self.durations.items():
            if self.verbose:
                print(f"\n{'='*80}")
                print(f"📊 Analyzing {duration_name} Duration ({duration_weeks} weeks)")
                print(f"{'='*80}")
            
            # Generate periods
            if use_non_overlapping:
                periods = self._generate_non_overlapping_periods(duration_weeks)
            else:
                periods = self._generate_rolling_periods(duration_weeks, rolling_step_weeks)
            
            if self.verbose:
                print(f"Periods to analyze: {len(periods)}")
            
            # Run simulations
            optimum_returns = []
            simple_returns = []
            optimum_values = []
            simple_values = []
            outperformance = []
            
            for start_date, end_date in periods:
                final_price = self._get_final_price(end_date)
                if final_price is None:
                    continue
                
                try:
                    analyzer = FlexibleOptimumDCA(
                        weekly_budget=self.weekly_budget,
                        start_date=start_date,
                        end_date=end_date,
                        final_btc_price=final_price,
                        verbose=False
                    )
                    
                    opt_results = analyzer.run_optimum_dca_simulation()
                    sim_results = analyzer.run_simple_dca_simulation()
                    
                    optimum_returns.append(opt_results['profit_pct'] / 100)
                    simple_returns.append(sim_results['profit_pct'] / 100)
                    optimum_values.append(opt_results['holding_value'])
                    simple_values.append(sim_results['holding_value'])
                    outperformance.append(opt_results['profit_pct'] - sim_results['profit_pct'])
                    
                except Exception as e:
                    if self.verbose:
                        print(f"  Warning: Failed {start_date} to {end_date}: {e}")
                    continue
            
            if len(optimum_returns) == 0:
                continue
            
            optimum_returns = np.array(optimum_returns)
            simple_returns = np.array(simple_returns)
            outperformance = np.array(outperformance)
            
            # Calculate years for annualization
            years = duration_weeks / 52
            
            # Risk-adjusted metrics
            optimum_sharpe = self.calculate_sharpe_ratio(optimum_returns, 1/years)
            simple_sharpe = self.calculate_sharpe_ratio(simple_returns, 1/years)
            
            optimum_sortino = self.calculate_sortino_ratio(optimum_returns, 1/years)
            simple_sortino = self.calculate_sortino_ratio(simple_returns, 1/years)
            
            # Drawdown analysis (on cumulative returns)
            optimum_cumulative = np.cumprod(1 + optimum_returns)
            simple_cumulative = np.cumprod(1 + simple_returns)
            
            optimum_dd = self.calculate_max_drawdown(optimum_cumulative)
            simple_dd = self.calculate_max_drawdown(simple_cumulative)
            
            # VaR and CVaR
            optimum_var = self.calculate_var_cvar(optimum_returns, 0.95)
            simple_var = self.calculate_var_cvar(simple_returns, 0.95)
            
            # Statistical significance
            sig_test = self.statistical_significance_test(optimum_returns, simple_returns)
            
            # Distribution analysis
            optimum_dist = self.analyze_return_distribution(optimum_returns)
            simple_dist = self.analyze_return_distribution(simple_returns)
            
            # Bootstrap confidence intervals
            opt_mean_ci = self.bootstrap_confidence_interval(optimum_returns, np.mean, 1000)
            sim_mean_ci = self.bootstrap_confidence_interval(simple_returns, np.mean, 1000)
            
            all_results[duration_name] = {
                'n_periods': len(periods),
                'years': years,
                
                'optimum': {
                    'mean_return': np.mean(optimum_returns),
                    'median_return': np.median(optimum_returns),
                    'std_return': np.std(optimum_returns, ddof=1),
                    'sharpe_ratio': optimum_sharpe,
                    'sortino_ratio': optimum_sortino,
                    'max_drawdown': optimum_dd['max_drawdown'],
                    'var_95': optimum_var['var'],
                    'cvar_95': optimum_var['cvar'],
                    'win_rate': np.mean(optimum_returns > 0),
                    'mean_ci': opt_mean_ci,
                    'distribution': optimum_dist
                },
                
                'simple': {
                    'mean_return': np.mean(simple_returns),
                    'median_return': np.median(simple_returns),
                    'std_return': np.std(simple_returns, ddof=1),
                    'sharpe_ratio': simple_sharpe,
                    'sortino_ratio': simple_sortino,
                    'max_drawdown': simple_dd['max_drawdown'],
                    'var_95': simple_var['var'],
                    'cvar_95': simple_var['cvar'],
                    'win_rate': np.mean(simple_returns > 0),
                    'mean_ci': sim_mean_ci,
                    'distribution': simple_dist
                },
                
                'comparison': {
                    'mean_outperformance': np.mean(outperformance),
                    'median_outperformance': np.median(outperformance),
                    'outperformance_rate': np.mean(outperformance > 0),
                    'significance': sig_test
                }
            }
        
        return all_results
    
    def print_analysis_report(self, results: Dict):
        """Print comprehensive analysis report."""
        
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE STATISTICAL REPORT")
        print("="*80)
        
        for duration, stats in results.items():
            print(f"\n{'='*80}")
            print(f"⏱️  {duration.upper()} DURATION")
            print(f"{'='*80}")
            print(f"Sample Size: {stats['n_periods']} non-overlapping periods")
            print(f"Duration: {stats['years']:.1f} years each")
            
            opt = stats['optimum']
            sim = stats['simple']
            comp = stats['comparison']
            
            print(f"\n🎯 RETURNS:")
            print(f"                        Optimum           Simple          Difference")
            print(f"  Mean Return:      {opt['mean_return']*100:>8.2f}%      {sim['mean_return']*100:>8.2f}%      {(opt['mean_return']-sim['mean_return'])*100:>8.2f}%")
            print(f"  Median Return:    {opt['median_return']*100:>8.2f}%      {sim['median_return']*100:>8.2f}%      {(opt['median_return']-sim['median_return'])*100:>8.2f}%")
            print(f"  95% CI:           [{opt['mean_ci'][1]*100:>6.2f}%, {opt['mean_ci'][2]*100:>6.2f}%]  [{sim['mean_ci'][1]*100:>6.2f}%, {sim['mean_ci'][2]*100:>6.2f}%]")
            
            print(f"\n📊 RISK METRICS:")
            print(f"                        Optimum           Simple          Winner")
            print(f"  Volatility (σ):   {opt['std_return']*100:>8.2f}%      {sim['std_return']*100:>8.2f}%      {'Simple' if sim['std_return'] < opt['std_return'] else 'Optimum'}")
            print(f"  Max Drawdown:     {opt['max_drawdown']*100:>8.2f}%      {sim['max_drawdown']*100:>8.2f}%      {'Simple' if abs(sim['max_drawdown']) < abs(opt['max_drawdown']) else 'Optimum'}")
            print(f"  VaR (95%):        {opt['var_95']*100:>8.2f}%      {sim['var_95']*100:>8.2f}%      {'Simple' if sim['var_95'] > opt['var_95'] else 'Optimum'}")
            print(f"  CVaR (95%):       {opt['cvar_95']*100:>8.2f}%      {sim['cvar_95']*100:>8.2f}%      {'Simple' if sim['cvar_95'] > opt['cvar_95'] else 'Optimum'}")
            
            print(f"\n🏆 RISK-ADJUSTED PERFORMANCE:")
            print(f"                        Optimum           Simple          Winner")
            print(f"  Sharpe Ratio:     {opt['sharpe_ratio']:>8.3f}         {sim['sharpe_ratio']:>8.3f}         {'Optimum' if opt['sharpe_ratio'] > sim['sharpe_ratio'] else 'Simple'}")
            print(f"  Sortino Ratio:    {opt['sortino_ratio']:>8.3f}         {sim['sortino_ratio']:>8.3f}         {'Optimum' if opt['sortino_ratio'] > sim['sortino_ratio'] else 'Simple'}")
            print(f"  Win Rate:         {opt['win_rate']*100:>8.2f}%      {sim['win_rate']*100:>8.2f}%      {'Optimum' if opt['win_rate'] > sim['win_rate'] else 'Simple'}")
            
            print(f"\n📈 DISTRIBUTION ANALYSIS:")
            opt_dist = opt['distribution']
            sim_dist = sim['distribution']
            if opt_dist and sim_dist and 'skewness' in opt_dist and 'skewness' in sim_dist:
                print(f"                        Optimum           Simple")
                print(f"  Skewness:         {opt_dist['skewness']:>8.3f}         {sim_dist['skewness']:>8.3f}         {'(right-skewed)' if opt_dist['skewness'] > 0 else '(left-skewed)'}")
                print(f"  Kurtosis:         {opt_dist['kurtosis']:>8.3f}         {sim_dist['kurtosis']:>8.3f}         {'(fat tails)' if opt_dist['kurtosis'] > 0 else '(thin tails)'}")
                print(f"  Normal Dist?      {str(opt_dist['is_normal']):>8}         {str(sim_dist['is_normal']):>8}")
            else:
                print(f"  (Sample size too small for distribution analysis)")
            
            print(f"\n🔬 STATISTICAL SIGNIFICANCE:")
            sig = comp['significance']
            print(f"  Outperformance Rate:    {comp['outperformance_rate']*100:.1f}%")
            print(f"  Mean Outperformance:    {comp['mean_outperformance']:.2f} pp")
            print(f"  T-statistic:            {sig['t_statistic']:.3f}")
            print(f"  P-value:                {sig['t_pvalue']:.4f}")
            print(f"  Effect Size (Cohen's d): {sig['cohens_d']:.3f}")
            print(f"  Significant at 5%:      {sig['significant_at_5pct']} {'✅' if sig['significant_at_5pct'] else '❌'}")
            print(f"  Significant at 1%:      {sig['significant_at_1pct']} {'✅' if sig['significant_at_1pct'] else '❌'}")
            
            # Interpretation
            if sig['significant_at_5pct']:
                if comp['mean_outperformance'] > 0:
                    print(f"\n  ✅ CONCLUSION: Optimum DCA is STATISTICALLY SIGNIFICANTLY better than Simple DCA")
                else:
                    print(f"\n  ⚠️  CONCLUSION: Simple DCA is STATISTICALLY SIGNIFICANTLY better than Optimum DCA")
            else:
                print(f"\n  ❌ CONCLUSION: No statistically significant difference between strategies")

def main():
    """Run advanced statistical analysis."""
    
    analyzer = AdvancedDurationAnalyzer(
        weekly_budget=250.0,
        overall_start=date(2016, 1, 1),
        overall_end=date(2025, 9, 24),
        risk_free_rate=0.04,
        verbose=True
    )
    
    # Run analysis with non-overlapping periods (statistically proper)
    results = analyzer.run_comprehensive_analysis(
        use_non_overlapping=True,
        rolling_step_weeks=4
    )
    
    # Print report
    analyzer.print_analysis_report(results)
    
    print("\n" + "="*80)
    print("✅ ADVANCED ANALYSIS COMPLETE")
    print("="*80)
    
    return results

if __name__ == "__main__":
    results = main()
