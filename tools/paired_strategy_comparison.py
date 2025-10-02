#!/usr/bin/env python3
"""
PAIRED STRATEGY COMPARISON ANALYZER

Implements proper paired statistical testing for DCA strategies.
Key innovation: Tracks SAME investment periods for both strategies to enable paired tests.

Advantages:
1. More statistical power than unpaired tests
2. Controls for market conditions (both strategies face same market)
3. Enables correlation analysis between strategies
4. Proper paired confidence intervals
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple, Optional
from scipy import stats
from scipy.stats import wilcoxon, ttest_rel, pearsonr, spearmanr
from sklearn.metrics import mean_absolute_error, mean_squared_error
import seaborn as sns
import matplotlib.pyplot as plt

from src.optimum_dca_analyzer import FlexibleOptimumDCA

class PairedStrategyComparison:
    """
    Paired comparison analyzer for DCA strategies.
    Ensures both strategies are tested on identical periods.
    """

    def __init__(self,
                 weekly_budget: float = 250.0,
                 overall_start: date = date(2016, 1, 1),
                 overall_end: date = date(2025, 9, 24)):
        """Initialize paired comparison analyzer."""
        self.weekly_budget = weekly_budget
        self.overall_start = overall_start
        self.overall_end = overall_end
        self.paired_results = []

    def run_paired_simulation(self, start_date: date, end_date: date) -> Dict:
        """
        Run both strategies on EXACTLY the same period.
        This enables proper paired statistical testing.
        """
        # Create analyzer for this specific period
        analyzer = FlexibleOptimumDCA(
            weekly_budget=self.weekly_budget,
            start_date=start_date,
            end_date=end_date,
            verbose=False
        )

        # Run both strategies on SAME data
        optimum = analyzer.run_optimum_dca_simulation()
        simple = analyzer.run_simple_dca_simulation()

        # Calculate paired differences
        return {
            'start_date': start_date,
            'end_date': end_date,
            'duration_weeks': (end_date - start_date).days // 7,
            'optimum_return': optimum['profit_pct'],
            'simple_return': simple['profit_pct'],
            'return_difference': optimum['profit_pct'] - simple['profit_pct'],
            'optimum_btc': optimum['total_btc'],
            'simple_btc': simple['total_btc'],
            'btc_difference': optimum['total_btc'] - simple['total_btc'],
            'optimum_investment': optimum['total_investment'],
            'simple_investment': simple['total_investment'],
            'optimum_value': optimum['holding_value'],
            'simple_value': simple['holding_value']
        }

    def generate_paired_samples(self, duration_weeks: int,
                              step_weeks: int = 4) -> List[Dict]:
        """
        Generate paired samples with controlled overlap.
        Both strategies evaluated on identical periods.
        """
        paired_results = []
        current_date = self.overall_start

        while True:
            end_date = current_date + timedelta(weeks=duration_weeks)

            if end_date > self.overall_end:
                break

            # Run paired simulation
            result = self.run_paired_simulation(current_date, end_date)
            paired_results.append(result)

            # Move to next period
            current_date = current_date + timedelta(weeks=step_weeks)

        return paired_results

    def paired_statistical_tests(self, differences: np.ndarray) -> Dict:
        """
        Comprehensive paired statistical testing.
        More powerful than unpaired tests.
        """
        n = len(differences)

        # 1. Paired t-test (parametric)
        t_stat, t_pvalue = ttest_rel(differences, np.zeros(n))

        # 2. Wilcoxon signed-rank test (non-parametric)
        if n > 0 and not np.all(differences == 0):
            w_stat, w_pvalue = wilcoxon(differences)
        else:
            w_stat, w_pvalue = np.nan, np.nan

        # 3. Sign test (most robust, least powerful)
        n_positive = np.sum(differences > 0)
        n_negative = np.sum(differences < 0)
        n_total = n_positive + n_negative
        if n_total > 0:
            sign_pvalue = 2 * stats.binom.cdf(min(n_positive, n_negative), n_total, 0.5)
        else:
            sign_pvalue = np.nan

        # 4. Effect size (Cohen's d for paired data)
        mean_diff = np.mean(differences)
        std_diff = np.std(differences, ddof=1) if n > 1 else 0
        cohens_d = mean_diff / std_diff if std_diff > 0 else 0

        # 5. Confidence interval for mean difference
        if n > 1:
            se = std_diff / np.sqrt(n)
            ci_lower = mean_diff - 1.96 * se
            ci_upper = mean_diff + 1.96 * se
        else:
            ci_lower, ci_upper = np.nan, np.nan

        return {
            'n_pairs': n,
            'mean_difference': mean_diff,
            'std_difference': std_diff,
            'paired_t_statistic': t_stat,
            'paired_t_pvalue': t_pvalue,
            'wilcoxon_statistic': w_stat,
            'wilcoxon_pvalue': w_pvalue,
            'sign_test_pvalue': sign_pvalue,
            'cohens_d': cohens_d,
            'ci_95_lower': ci_lower,
            'ci_95_upper': ci_upper,
            'n_optimum_wins': n_positive,
            'n_simple_wins': n_negative,
            'win_rate_optimum': n_positive / n_total if n_total > 0 else np.nan
        }

    def correlation_analysis(self, optimum_returns: np.ndarray,
                           simple_returns: np.ndarray) -> Dict:
        """
        Analyze correlation between strategies.
        High correlation suggests similar market exposure.
        """
        if len(optimum_returns) < 2 or len(simple_returns) < 2:
            return {}

        # Pearson correlation (linear)
        pearson_r, pearson_p = pearsonr(optimum_returns, simple_returns)

        # Spearman correlation (monotonic)
        spearman_r, spearman_p = spearmanr(optimum_returns, simple_returns)

        # Beta (regression coefficient)
        # How much Optimum moves relative to Simple
        X = simple_returns.reshape(-1, 1)
        y = optimum_returns
        if len(X) > 1:
            from sklearn.linear_model import LinearRegression
            reg = LinearRegression().fit(X, y)
            beta = reg.coef_[0]
            alpha = reg.intercept_
            r_squared = reg.score(X, y)
        else:
            beta, alpha, r_squared = np.nan, np.nan, np.nan

        return {
            'pearson_correlation': pearson_r,
            'pearson_pvalue': pearson_p,
            'spearman_correlation': spearman_r,
            'spearman_pvalue': spearman_p,
            'beta': beta,  # Optimum sensitivity to Simple
            'alpha': alpha,  # Optimum excess return
            'r_squared': r_squared,
            'correlation_interpretation': 'High' if abs(pearson_r) > 0.7 else 'Medium' if abs(pearson_r) > 0.3 else 'Low'
        }

    def consistency_analysis(self, differences: np.ndarray) -> Dict:
        """
        Analyze consistency of outperformance.
        Is one strategy consistently better or does it vary?
        """
        if len(differences) == 0:
            return {}

        # Calculate runs (consecutive wins/losses)
        signs = np.sign(differences)
        runs = []
        current_run = 1

        for i in range(1, len(signs)):
            if signs[i] == signs[i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)

        # Maximum winning/losing streak
        positive_runs = [runs[i] for i in range(len(runs)) if signs[np.sum(runs[:i]) if i > 0 else 0] > 0]
        negative_runs = [runs[i] for i in range(len(runs)) if signs[np.sum(runs[:i]) if i > 0 else 0] < 0]

        max_win_streak = max(positive_runs) if positive_runs else 0
        max_loss_streak = max(negative_runs) if negative_runs else 0

        # Consistency ratio
        consistency_ratio = np.std(differences) / np.abs(np.mean(differences)) if np.mean(differences) != 0 else np.inf

        return {
            'total_periods': len(differences),
            'consistent_winner': 'Optimum' if np.mean(differences) > 0 else 'Simple',
            'max_optimum_streak': max_win_streak,
            'max_simple_streak': max_loss_streak,
            'n_regime_changes': len(runs) - 1,
            'consistency_ratio': consistency_ratio,
            'consistency_interpretation': 'Very consistent' if consistency_ratio < 0.5 else 'Moderately consistent' if consistency_ratio < 1 else 'Inconsistent'
        }

    def risk_adjusted_comparison(self, paired_results: List[Dict]) -> Dict:
        """
        Compare risk-adjusted performance using paired data.
        """
        optimum_returns = np.array([r['optimum_return'] for r in paired_results])
        simple_returns = np.array([r['simple_return'] for r in paired_results])
        differences = optimum_returns - simple_returns

        # Sharpe ratio difference
        optimum_sharpe = np.mean(optimum_returns) / np.std(optimum_returns) if np.std(optimum_returns) > 0 else 0
        simple_sharpe = np.mean(simple_returns) / np.std(simple_returns) if np.std(simple_returns) > 0 else 0
        sharpe_difference = optimum_sharpe - simple_sharpe

        # Information ratio (risk-adjusted outperformance)
        tracking_error = np.std(differences, ddof=1) if len(differences) > 1 else 0
        information_ratio = np.mean(differences) / tracking_error if tracking_error > 0 else 0

        # Maximum relative drawdown
        cumulative_diff = np.cumsum(differences)
        running_max = np.maximum.accumulate(cumulative_diff)
        relative_drawdown = (cumulative_diff - running_max)
        max_relative_drawdown = np.min(relative_drawdown) if len(relative_drawdown) > 0 else 0

        return {
            'optimum_sharpe': optimum_sharpe,
            'simple_sharpe': simple_sharpe,
            'sharpe_difference': sharpe_difference,
            'information_ratio': information_ratio,
            'tracking_error': tracking_error,
            'max_relative_drawdown': max_relative_drawdown,
            'risk_adjusted_winner': 'Optimum' if sharpe_difference > 0 else 'Simple'
        }

    def run_comprehensive_paired_analysis(self, durations: List[int] = [52, 104, 156, 208]) -> Dict:
        """
        Run comprehensive paired analysis for multiple durations.
        """
        print("="*80)
        print(" PAIRED STRATEGY COMPARISON ANALYSIS")
        print("="*80)
        print("Using paired tests for maximum statistical power")
        print()

        all_results = {}

        for duration_weeks in durations:
            duration_name = f'{duration_weeks//52}Y'
            print(f"\n ANALYZING {duration_name} DURATION")
            print("-"*40)

            # Generate paired samples
            paired_results = self.generate_paired_samples(duration_weeks, step_weeks=4)

            if not paired_results:
                print(f"  No data available for {duration_name}")
                continue

            # Extract arrays for analysis
            optimum_returns = np.array([r['optimum_return'] for r in paired_results])
            simple_returns = np.array([r['simple_return'] for r in paired_results])
            differences = optimum_returns - simple_returns

            # Run all analyses
            statistical_tests = self.paired_statistical_tests(differences)
            correlation = self.correlation_analysis(optimum_returns, simple_returns)
            consistency = self.consistency_analysis(differences)
            risk_adjusted = self.risk_adjusted_comparison(paired_results)

            # Store results
            all_results[duration_name] = {
                'paired_samples': len(paired_results),
                'mean_optimum_return': np.mean(optimum_returns),
                'mean_simple_return': np.mean(simple_returns),
                'mean_difference': statistical_tests['mean_difference'],
                'statistical_tests': statistical_tests,
                'correlation': correlation,
                'consistency': consistency,
                'risk_adjusted': risk_adjusted
            }

            # Print summary
            print(f"  Paired samples: {len(paired_results)}")
            print(f"  Mean returns: Optimum={np.mean(optimum_returns):.1f}%, Simple={np.mean(simple_returns):.1f}%")
            print(f"  Mean difference: {statistical_tests['mean_difference']:.1f}pp")
            print(f"  95% CI: [{statistical_tests['ci_95_lower']:.1f}, {statistical_tests['ci_95_upper']:.1f}]")
            print(f"  Paired t-test p-value: {statistical_tests['paired_t_pvalue']:.4f}")
            print(f"  Wilcoxon p-value: {statistical_tests['wilcoxon_pvalue']:.4f}")
            print(f"  Win rate (Optimum): {statistical_tests['win_rate_optimum']:.1%}")
            print(f"  Correlation: {correlation.get('pearson_correlation', np.nan):.3f}")
            print(f"  Information ratio: {risk_adjusted['information_ratio']:.3f}")
            print(f"  Risk-adjusted winner: {risk_adjusted['risk_adjusted_winner']}")

        return all_results

    def plot_paired_analysis(self, paired_results: List[Dict], duration_name: str):
        """
        Visualize paired comparison results.
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        optimum_returns = [r['optimum_return'] for r in paired_results]
        simple_returns = [r['simple_return'] for r in paired_results]
        differences = [r['return_difference'] for r in paired_results]

        # 1. Scatter plot of paired returns
        ax = axes[0, 0]
        ax.scatter(simple_returns, optimum_returns, alpha=0.6)
        ax.plot([min(simple_returns), max(simple_returns)],
                [min(simple_returns), max(simple_returns)], 'r--', label='Equal performance')
        ax.set_xlabel('Simple DCA Return (%)')
        ax.set_ylabel('Optimum DCA Return (%)')
        ax.set_title(f'Paired Returns - {duration_name}')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Distribution of differences
        ax = axes[0, 1]
        ax.hist(differences, bins=20, alpha=0.7, edgecolor='black')
        ax.axvline(0, color='red', linestyle='--', label='No difference')
        ax.axvline(np.mean(differences), color='green', linestyle='-', label=f'Mean: {np.mean(differences):.1f}pp')
        ax.set_xlabel('Return Difference (Optimum - Simple) pp')
        ax.set_ylabel('Frequency')
        ax.set_title('Distribution of Paired Differences')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 3. Time series of differences
        ax = axes[1, 0]
        dates = [r['start_date'] for r in paired_results]
        ax.plot(dates, differences, marker='o', markersize=4)
        ax.axhline(0, color='red', linestyle='--', alpha=0.5)
        ax.fill_between(dates, 0, differences,
                        where=[d > 0 for d in differences],
                        alpha=0.3, color='green', label='Optimum wins')
        ax.fill_between(dates, 0, differences,
                        where=[d <= 0 for d in differences],
                        alpha=0.3, color='red', label='Simple wins')
        ax.set_xlabel('Start Date')
        ax.set_ylabel('Return Difference (pp)')
        ax.set_title('Performance Difference Over Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # 4. Cumulative difference
        ax = axes[1, 1]
        cumulative_diff = np.cumsum(differences)
        ax.plot(dates, cumulative_diff, linewidth=2)
        ax.fill_between(dates, 0, cumulative_diff, alpha=0.3)
        ax.axhline(0, color='red', linestyle='--', alpha=0.5)
        ax.set_xlabel('Start Date')
        ax.set_ylabel('Cumulative Difference (pp)')
        ax.set_title('Cumulative Performance Difference')
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.suptitle(f'Paired Strategy Comparison - {duration_name}', fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save figure
        filename = f'reports/analysis/paired_comparison_{duration_name}.png'
        os.makedirs('reports/analysis', exist_ok=True)
        plt.savefig(filename, dpi=100)
        plt.close()

        print(f"   Visualization saved to: {filename}")

def main():
    """Run paired comparison analysis."""
    analyzer = PairedStrategyComparison()
    results = analyzer.run_comprehensive_paired_analysis()

    print("\n" + "="*80)
    print(" SUMMARY OF PAIRED ANALYSIS")
    print("="*80)

    # Summary table
    print("\nStatistical Significance (p < 0.05):")
    print("-"*40)
    for duration, data in results.items():
        p_value = data['statistical_tests']['paired_t_pvalue']
        significant = "YES " if p_value < 0.05 else "NO "
        winner = data['consistency']['consistent_winner']
        print(f"{duration}: p={p_value:.4f} - {significant} - Winner: {winner}")

    print("\nRisk-Adjusted Performance:")
    print("-"*40)
    for duration, data in results.items():
        ir = data['risk_adjusted']['information_ratio']
        winner = data['risk_adjusted']['risk_adjusted_winner']
        print(f"{duration}: IR={ir:.3f} - Winner: {winner}")

    print("\n" + "="*80)
    print(" PAIRED ANALYSIS COMPLETE")
    print("="*80)
    print("\n KEY ADVANTAGES OF PAIRED TESTING:")
    print("  1. Higher statistical power (same market conditions)")
    print("  2. Controls for external factors")
    print("  3. Enables correlation analysis")
    print("  4. More accurate confidence intervals")
    print("  5. Better for investment decision-making")

    return results

if __name__ == "__main__":
    results = main()