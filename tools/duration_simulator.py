#!/usr/bin/env python3
"""
INVESTMENT DURATION SIMULATOR

Runs comprehensive simulations for 1-year, 2-year, 3-year, and 4-year investment 
durations between 1-1-2016 and 9-24-2025. Compares Optimum DCA vs Simple DCA 
performance across all possible time periods.

Features:
- Maximum permutations: Weekly start dates for all durations
- Performance aggregation by duration
- Comprehensive statistical analysis
- Detailed and summary reports
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

from src.optimum_dca_analyzer import FlexibleOptimumDCA

class DurationSimulator:
    """
    Simulates investment performance across different durations.
    
    Args:
        weekly_budget: Weekly investment amount
        overall_start: Earliest possible start date
        overall_end: Latest possible end date
        verbose: Print progress updates
    """
    
    def __init__(self, 
                 weekly_budget: float = 250.0,
                 overall_start: date = date(2016, 1, 1),
                 overall_end: date = date(2025, 9, 24),
                 verbose: bool = True):
        
        self.weekly_budget = weekly_budget
        self.overall_start = overall_start
        self.overall_end = overall_end
        self.verbose = verbose
        
        # Duration definitions (in weeks)
        self.durations = {
            '1-Year': 52,
            '2-Year': 104,
            '3-Year': 156,
            '4-Year': 208
        }
        
        # Load price data once for efficiency
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
        # Find the closest price on or before the end date
        valid_prices = self.price_data[self.price_data['date_only'] <= end_date]
        if len(valid_prices) == 0:
            return None
        return valid_prices.iloc[-1]['Price']
    
    def _generate_start_dates(self, duration_weeks: int) -> List[date]:
        """Generate all valid start dates for a given duration."""
        start_dates = []
        current_date = self.overall_start
        
        while True:
            # Calculate end date for this duration
            end_date = current_date + timedelta(weeks=duration_weeks)
            
            # Check if end date is within our overall range
            if end_date > self.overall_end:
                break
                
            start_dates.append(current_date)
            # Move to next week
            current_date = current_date + timedelta(weeks=1)
        
        return start_dates
    
    def _run_single_simulation(self, 
                               start_date: date, 
                               end_date: date,
                               duration_name: str) -> Dict:
        """Run both Optimum and Simple DCA for a single period."""
        
        # Get final BTC price for this period
        final_price = self._get_final_price(end_date)
        if final_price is None:
            return None
        
        try:
            # Create analyzer with verbose=False for batch processing
            analyzer = FlexibleOptimumDCA(
                weekly_budget=self.weekly_budget,
                start_date=start_date,
                end_date=end_date,
                final_btc_price=final_price,
                verbose=False
            )
            
            # Run both strategies
            optimum_results = analyzer.run_optimum_dca_simulation()
            simple_results = analyzer.run_simple_dca_simulation()
            
            # Calculate outperformance
            outperformance = optimum_results['profit_pct'] - simple_results['profit_pct']
            outperformance_ratio = optimum_results['profit_pct'] / simple_results['profit_pct'] if simple_results['profit_pct'] > 0 else 0
            
            return {
                'duration': duration_name,
                'start_date': start_date,
                'end_date': end_date,
                'weeks': optimum_results['period_weeks'],
                'final_btc_price': final_price,
                
                # Optimum DCA results
                'optimum_btc': optimum_results['total_btc'],
                'optimum_investment': optimum_results['total_investment'],
                'optimum_value': optimum_results['holding_value'],
                'optimum_profit': optimum_results['profit'],
                'optimum_return_pct': optimum_results['profit_pct'],
                
                # Simple DCA results
                'simple_btc': simple_results['total_btc'],
                'simple_investment': simple_results['total_investment'],
                'simple_value': simple_results['holding_value'],
                'simple_profit': simple_results['profit'],
                'simple_return_pct': simple_results['profit_pct'],
                
                # Comparison
                'outperformance_pct': outperformance,
                'outperformance_ratio': outperformance_ratio,
            }
            
        except Exception as e:
            if self.verbose:
                print(f" Error simulating {start_date} to {end_date}: {e}")
            return None
    
    def run_all_simulations(self) -> pd.DataFrame:
        """Run all simulations for all durations."""
        
        print("="*80)
        print(" INVESTMENT DURATION SIMULATOR")
        print("="*80)
        print(f"Overall Period: {self.overall_start} to {self.overall_end}")
        print(f"Weekly Budget: ${self.weekly_budget:.2f}")
        print(f"Durations: {', '.join(self.durations.keys())}")
        print("="*80)
        
        all_results = []
        total_simulations = 0
        
        # Calculate total number of simulations
        for duration_name, duration_weeks in self.durations.items():
            start_dates = self._generate_start_dates(duration_weeks)
            total_simulations += len(start_dates)
        
        print(f"\n Total simulations to run: {total_simulations:,}")
        print()
        
        current_sim = 0
        
        # Run simulations for each duration
        for duration_name, duration_weeks in self.durations.items():
            if self.verbose:
                print(f"\n{'='*80}")
                print(f"⏱️  Processing {duration_name} Duration ({duration_weeks} weeks)")
                print(f"{'='*80}")
            
            # Generate all start dates for this duration
            start_dates = self._generate_start_dates(duration_weeks)
            
            if self.verbose:
                print(f"   Start dates: {len(start_dates):,}")
            
            # Run simulation for each start date
            for i, start_date in enumerate(start_dates):
                end_date = start_date + timedelta(weeks=duration_weeks)
                
                result = self._run_single_simulation(start_date, end_date, duration_name)
                if result:
                    all_results.append(result)
                
                current_sim += 1
                
                # Progress update every 50 simulations
                if self.verbose and (i + 1) % 50 == 0:
                    print(f"   Progress: {i+1:,}/{len(start_dates):,} ({(i+1)/len(start_dates)*100:.1f}%) | "
                          f"Overall: {current_sim:,}/{total_simulations:,} ({current_sim/total_simulations*100:.1f}%)")
        
        if self.verbose:
            print(f"\n{'='*80}")
            print(f" Completed {len(all_results):,} simulations successfully")
            print(f"{'='*80}\n")
        
        # Convert to DataFrame
        results_df = pd.DataFrame(all_results)
        return results_df
    
    def generate_summary_statistics(self, results_df: pd.DataFrame) -> Dict:
        """Generate comprehensive summary statistics."""
        
        summary = {}
        
        for duration in self.durations.keys():
            duration_data = results_df[results_df['duration'] == duration]
            
            if len(duration_data) == 0:
                continue
            
            summary[duration] = {
                'total_runs': len(duration_data),
                
                # Optimum DCA statistics
                'optimum': {
                    'avg_return': duration_data['optimum_return_pct'].mean(),
                    'median_return': duration_data['optimum_return_pct'].median(),
                    'min_return': duration_data['optimum_return_pct'].min(),
                    'max_return': duration_data['optimum_return_pct'].max(),
                    'std_return': duration_data['optimum_return_pct'].std(),
                    'avg_btc': duration_data['optimum_btc'].mean(),
                    'avg_investment': duration_data['optimum_investment'].mean(),
                    'avg_value': duration_data['optimum_value'].mean(),
                    'win_rate': (duration_data['optimum_return_pct'] > 0).sum() / len(duration_data) * 100,
                },
                
                # Simple DCA statistics
                'simple': {
                    'avg_return': duration_data['simple_return_pct'].mean(),
                    'median_return': duration_data['simple_return_pct'].median(),
                    'min_return': duration_data['simple_return_pct'].min(),
                    'max_return': duration_data['simple_return_pct'].max(),
                    'std_return': duration_data['simple_return_pct'].std(),
                    'avg_btc': duration_data['simple_btc'].mean(),
                    'avg_investment': duration_data['simple_investment'].mean(),
                    'avg_value': duration_data['simple_value'].mean(),
                    'win_rate': (duration_data['simple_return_pct'] > 0).sum() / len(duration_data) * 100,
                },
                
                # Outperformance statistics
                'outperformance': {
                    'avg_pct_points': duration_data['outperformance_pct'].mean(),
                    'median_pct_points': duration_data['outperformance_pct'].median(),
                    'min_pct_points': duration_data['outperformance_pct'].min(),
                    'max_pct_points': duration_data['outperformance_pct'].max(),
                    'times_better': (duration_data['outperformance_pct'] > 0).sum() / len(duration_data) * 100,
                    'avg_ratio': duration_data['outperformance_ratio'].mean(),
                }
            }
        
        # Calculate blended (overall) statistics
        summary['Blended'] = {
            'total_runs': len(results_df),
            
            'optimum': {
                'avg_return': results_df['optimum_return_pct'].mean(),
                'median_return': results_df['optimum_return_pct'].median(),
                'min_return': results_df['optimum_return_pct'].min(),
                'max_return': results_df['optimum_return_pct'].max(),
                'std_return': results_df['optimum_return_pct'].std(),
                'avg_btc': results_df['optimum_btc'].mean(),
                'avg_investment': results_df['optimum_investment'].mean(),
                'avg_value': results_df['optimum_value'].mean(),
                'win_rate': (results_df['optimum_return_pct'] > 0).sum() / len(results_df) * 100,
            },
            
            'simple': {
                'avg_return': results_df['simple_return_pct'].mean(),
                'median_return': results_df['simple_return_pct'].median(),
                'min_return': results_df['simple_return_pct'].min(),
                'max_return': results_df['simple_return_pct'].max(),
                'std_return': results_df['simple_return_pct'].std(),
                'avg_btc': results_df['simple_btc'].mean(),
                'avg_investment': results_df['simple_investment'].mean(),
                'avg_value': results_df['simple_value'].mean(),
                'win_rate': (results_df['simple_return_pct'] > 0).sum() / len(results_df) * 100,
            },
            
            'outperformance': {
                'avg_pct_points': results_df['outperformance_pct'].mean(),
                'median_pct_points': results_df['outperformance_pct'].median(),
                'min_pct_points': results_df['outperformance_pct'].min(),
                'max_pct_points': results_df['outperformance_pct'].max(),
                'times_better': (results_df['outperformance_pct'] > 0).sum() / len(results_df) * 100,
                'avg_ratio': results_df['outperformance_ratio'].mean(),
            }
        }
        
        return summary
    
    def print_summary_report(self, summary: Dict):
        """Print comprehensive summary report."""
        
        print("\n" + "="*80)
        print(" COMPREHENSIVE PERFORMANCE SUMMARY")
        print("="*80)
        
        # Print summary for each duration
        for duration in ['1-Year', '2-Year', '3-Year', '4-Year', 'Blended']:
            if duration not in summary:
                continue
            
            stats = summary[duration]
            
            print(f"\n{'='*80}")
            print(f"⏱️  {duration.upper()} DURATION")
            print(f"{'='*80}")
            print(f"Total Simulations: {stats['total_runs']:,}")
            
            print(f"\n OPTIMUM DCA PERFORMANCE:")
            print(f"   Average Return:    {stats['optimum']['avg_return']:>10.2f}%")
            print(f"   Median Return:     {stats['optimum']['median_return']:>10.2f}%")
            print(f"   Return Range:      {stats['optimum']['min_return']:>10.2f}% to {stats['optimum']['max_return']:>10.2f}%")
            print(f"   Std Deviation:     {stats['optimum']['std_return']:>10.2f}%")
            print(f"   Win Rate:          {stats['optimum']['win_rate']:>10.1f}%")
            print(f"   Avg Investment:    ${stats['optimum']['avg_investment']:>15,.2f}")
            print(f"   Avg Final Value:   ${stats['optimum']['avg_value']:>15,.2f}")
            print(f"   Avg BTC Acquired:  {stats['optimum']['avg_btc']:>10.8f}")
            
            print(f"\n SIMPLE DCA PERFORMANCE:")
            print(f"   Average Return:    {stats['simple']['avg_return']:>10.2f}%")
            print(f"   Median Return:     {stats['simple']['median_return']:>10.2f}%")
            print(f"   Return Range:      {stats['simple']['min_return']:>10.2f}% to {stats['simple']['max_return']:>10.2f}%")
            print(f"   Std Deviation:     {stats['simple']['std_return']:>10.2f}%")
            print(f"   Win Rate:          {stats['simple']['win_rate']:>10.1f}%")
            print(f"   Avg Investment:    ${stats['simple']['avg_investment']:>15,.2f}")
            print(f"   Avg Final Value:   ${stats['simple']['avg_value']:>15,.2f}")
            print(f"   Avg BTC Acquired:  {stats['simple']['avg_btc']:>10.8f}")
            
            print(f"\n🏆 OPTIMUM vs SIMPLE COMPARISON:")
            print(f"   Avg Outperformance:      {stats['outperformance']['avg_pct_points']:>10.2f} percentage points")
            print(f"   Median Outperformance:   {stats['outperformance']['median_pct_points']:>10.2f} percentage points")
            print(f"   Outperformance Range:    {stats['outperformance']['min_pct_points']:>10.2f} to {stats['outperformance']['max_pct_points']:>10.2f} pp")
            print(f"   Times Optimum Better:    {stats['outperformance']['times_better']:>10.1f}%")
            print(f"   Avg Return Multiplier:   {stats['outperformance']['avg_ratio']:>10.2f}x")
    
    def generate_detailed_report(self, results_df: pd.DataFrame, output_file: str = "duration_simulation_detailed_report.csv"):
        """Save detailed results to CSV."""
        
        # Sort by duration and start date
        results_df = results_df.sort_values(['duration', 'start_date'])
        
        # Save to CSV
        results_df.to_csv(output_file, index=False)
        print(f"\n💾 Detailed results saved to: {output_file}")
        print(f"   Total rows: {len(results_df):,}")
        
        return output_file
    
    def generate_summary_report(self, summary: Dict, output_file: str = "duration_simulation_summary_report.txt"):
        """Save summary report to text file."""
        
        with open(output_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("INVESTMENT DURATION SIMULATION - SUMMARY REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Period: {self.overall_start} to {self.overall_end}\n")
            f.write(f"Weekly Budget: ${self.weekly_budget:.2f}\n")
            f.write("="*80 + "\n\n")
            
            for duration in ['1-Year', '2-Year', '3-Year', '4-Year', 'Blended']:
                if duration not in summary:
                    continue
                
                stats = summary[duration]
                
                f.write("="*80 + "\n")
                f.write(f"{duration.upper()} DURATION\n")
                f.write("="*80 + "\n")
                f.write(f"Total Simulations: {stats['total_runs']:,}\n\n")
                
                f.write("OPTIMUM DCA PERFORMANCE:\n")
                f.write(f"  Average Return:    {stats['optimum']['avg_return']:>10.2f}%\n")
                f.write(f"  Median Return:     {stats['optimum']['median_return']:>10.2f}%\n")
                f.write(f"  Return Range:      {stats['optimum']['min_return']:>10.2f}% to {stats['optimum']['max_return']:>10.2f}%\n")
                f.write(f"  Std Deviation:     {stats['optimum']['std_return']:>10.2f}%\n")
                f.write(f"  Win Rate:          {stats['optimum']['win_rate']:>10.1f}%\n")
                f.write(f"  Avg Investment:    ${stats['optimum']['avg_investment']:>15,.2f}\n")
                f.write(f"  Avg Final Value:   ${stats['optimum']['avg_value']:>15,.2f}\n")
                f.write(f"  Avg BTC Acquired:  {stats['optimum']['avg_btc']:>10.8f}\n\n")
                
                f.write("SIMPLE DCA PERFORMANCE:\n")
                f.write(f"  Average Return:    {stats['simple']['avg_return']:>10.2f}%\n")
                f.write(f"  Median Return:     {stats['simple']['median_return']:>10.2f}%\n")
                f.write(f"  Return Range:      {stats['simple']['min_return']:>10.2f}% to {stats['simple']['max_return']:>10.2f}%\n")
                f.write(f"  Std Deviation:     {stats['simple']['std_return']:>10.2f}%\n")
                f.write(f"  Win Rate:          {stats['simple']['win_rate']:>10.1f}%\n")
                f.write(f"  Avg Investment:    ${stats['simple']['avg_investment']:>15,.2f}\n")
                f.write(f"  Avg Final Value:   ${stats['simple']['avg_value']:>15,.2f}\n")
                f.write(f"  Avg BTC Acquired:  {stats['simple']['avg_btc']:>10.8f}\n\n")
                
                f.write("OPTIMUM vs SIMPLE COMPARISON:\n")
                f.write(f"  Avg Outperformance:      {stats['outperformance']['avg_pct_points']:>10.2f} percentage points\n")
                f.write(f"  Median Outperformance:   {stats['outperformance']['median_pct_points']:>10.2f} percentage points\n")
                f.write(f"  Outperformance Range:    {stats['outperformance']['min_pct_points']:>10.2f} to {stats['outperformance']['max_pct_points']:>10.2f} pp\n")
                f.write(f"  Times Optimum Better:    {stats['outperformance']['times_better']:>10.1f}%\n")
                f.write(f"  Avg Return Multiplier:   {stats['outperformance']['avg_ratio']:>10.2f}x\n\n")
        
        print(f"💾 Summary report saved to: {output_file}")
        
        return output_file

def main():
    """Run the comprehensive duration simulation."""
    
    # Create simulator
    simulator = DurationSimulator(
        weekly_budget=250.0,
        overall_start=date(2016, 1, 1),
        overall_end=date(2025, 9, 24),
        verbose=True
    )
    
    # Run all simulations
    results_df = simulator.run_all_simulations()
    
    # Generate summary statistics
    summary = simulator.generate_summary_statistics(results_df)
    
    # Print summary report
    simulator.print_summary_report(summary)
    
    # Save detailed results
    simulator.generate_detailed_report(results_df)
    
    # Save summary report
    simulator.generate_summary_report(summary)
    
    print("\n" + "="*80)
    print(" SIMULATION COMPLETE")
    print("="*80)
    print("\nFiles generated:")
    print("  1. duration_simulation_detailed_report.csv - All simulation results")
    print("  2. duration_simulation_summary_report.txt  - Statistical summary")
    print("\n")
    
    return results_df, summary

if __name__ == "__main__":
    results_df, summary = main()
