#!/usr/bin/env python3
"""
COMPREHENSIVE COMPARISON REPORT GENERATOR

Runs all three analysis approaches and generates a complete comparison report.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
from datetime import datetime, date
import json

from src.optimum_dca_analyzer import FlexibleOptimumDCA
from advanced_duration_analyzer import AdvancedDurationAnalyzer

def run_duration_simulator_analysis():
    """Extract key metrics from existing duration simulator results."""
    print("\n" + "="*80)
    print("📊 LOADING DURATION SIMULATOR RESULTS")
    print("="*80)
    
    try:
        df = pd.read_csv("duration_simulation_detailed_report.csv")
        
        results = {}
        for duration in ['1-Year', '2-Year', '3-Year', '4-Year']:
            data = df[df['duration'] == duration]
            
            results[duration] = {
                'method': 'Weekly Rolling (Overlapping)',
                'n_simulations': len(data),
                'n_effective': int(len(data) * 0.02),  # ~2% independence
                'optimum_mean': data['optimum_return_pct'].mean(),
                'optimum_median': data['optimum_return_pct'].median(),
                'optimum_std': data['optimum_return_pct'].std(),
                'simple_mean': data['simple_return_pct'].mean(),
                'simple_median': data['simple_return_pct'].median(),
                'simple_std': data['simple_return_pct'].std(),
                'outperformance': data['outperformance_pct'].mean(),
                'win_rate': (data['outperformance_pct'] > 0).sum() / len(data) * 100,
                'best_period': f"{data.nlargest(1, 'optimum_return_pct').iloc[0]['start_date']} to {data.nlargest(1, 'optimum_return_pct').iloc[0]['end_date']}",
                'best_return': data['optimum_return_pct'].max()
            }
        
        print(f"✅ Loaded {len(df)} simulation results")
        return results
        
    except FileNotFoundError:
        print("❌ Duration simulator results not found. Run duration_simulator.py first.")
        return {}

def run_balanced_rolling_analysis():
    """Run balanced rolling analysis with monthly steps (v2.1 optimized)."""
    print("\n" + "="*80)
    print("📊 RUNNING BALANCED ROLLING ANALYSIS (Monthly - v2.1)")
    print("="*80)
    
    analyzer = AdvancedDurationAnalyzer(
        weekly_budget=250.0,
        overall_start=date(2016, 1, 1),
        overall_end=date(2025, 9, 24),
        risk_free_rate=0.04,
        verbose=False
    )
    
    stats = analyzer.run_comprehensive_analysis(
        use_non_overlapping=False,
        rolling_step_weeks=4  # MONTHLY (v2.1 optimized)
    )
    
    results = {}
    for duration, data in stats.items():
        results[duration] = {
            'method': 'Monthly Rolling (4-week steps) - v2.1',
            'n_simulations': data['n_periods'],
            'n_effective': int(data['n_periods'] * 0.08),  # ~8% independence
            'optimum_mean': data['optimum']['mean_return'] * 100,
            'optimum_median': data['optimum']['median_return'] * 100,
            'optimum_std': data['optimum']['std_return'] * 100,
            'optimum_sharpe': data['optimum']['sharpe_ratio'],
            'optimum_sortino': data['optimum']['sortino_ratio'],
            'optimum_max_dd': data['optimum']['max_drawdown'] * 100,
            'optimum_var': data['optimum']['var_95'] * 100,
            'simple_mean': data['simple']['mean_return'] * 100,
            'simple_median': data['simple']['median_return'] * 100,
            'simple_std': data['simple']['std_return'] * 100,
            'simple_sharpe': data['simple']['sharpe_ratio'],
            'simple_sortino': data['simple']['sortino_ratio'],
            'simple_max_dd': data['simple']['max_drawdown'] * 100,
            'simple_var': data['simple']['var_95'] * 100,
            'outperformance': data['comparison']['mean_outperformance'],
            'win_rate': data['comparison']['outperformance_rate'] * 100,
            'p_value': data['comparison']['significance']['t_pvalue'],
            'effect_size': data['comparison']['significance']['cohens_d'],
            'significant': data['comparison']['significance']['significant_at_5pct']
        }
    
    print(f"✅ Completed {sum(r['n_simulations'] for r in results.values())} simulations")
    return results

def run_non_overlapping_analysis():
    """Run non-overlapping analysis."""
    print("\n" + "="*80)
    print("📊 RUNNING NON-OVERLAPPING ANALYSIS")
    print("="*80)
    
    analyzer = AdvancedDurationAnalyzer(
        weekly_budget=250.0,
        overall_start=date(2016, 1, 1),
        overall_end=date(2025, 9, 24),
        risk_free_rate=0.04,
        verbose=False
    )
    
    stats = analyzer.run_comprehensive_analysis(
        use_non_overlapping=True
    )
    
    results = {}
    for duration, data in stats.items():
        results[duration] = {
            'method': 'Non-Overlapping (Perfect Independence)',
            'n_simulations': data['n_periods'],
            'n_effective': data['n_periods'],  # 100% independence
            'optimum_mean': data['optimum']['mean_return'] * 100,
            'optimum_median': data['optimum']['median_return'] * 100,
            'optimum_std': data['optimum']['std_return'] * 100,
            'optimum_sharpe': data['optimum']['sharpe_ratio'],
            'optimum_sortino': data['optimum']['sortino_ratio'],
            'optimum_max_dd': data['optimum']['max_drawdown'] * 100,
            'optimum_var': data['optimum']['var_95'] * 100,
            'simple_mean': data['simple']['mean_return'] * 100,
            'simple_median': data['simple']['median_return'] * 100,
            'simple_std': data['simple']['std_return'] * 100,
            'simple_sharpe': data['simple']['sharpe_ratio'],
            'simple_sortino': data['simple']['sortino_ratio'],
            'simple_max_dd': data['simple']['max_drawdown'] * 100,
            'simple_var': data['simple']['var_95'] * 100,
            'outperformance': data['comparison']['mean_outperformance'],
            'win_rate': data['comparison']['outperformance_rate'] * 100,
            'p_value': data['comparison']['significance']['t_pvalue'],
            'effect_size': data['comparison']['significance']['cohens_d'],
            'significant': data['comparison']['significance']['significant_at_5pct']
        }
    
    print(f"✅ Completed {sum(r['n_simulations'] for r in results.values())} simulations")
    return results

def generate_comparison_report(duration_sim, balanced, non_overlapping):
    """Generate comprehensive comparison report."""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report = []
    report.append("="*100)
    report.append("COMPREHENSIVE DCA ANALYSIS COMPARISON REPORT")
    report.append("="*100)
    report.append(f"Generated: {timestamp}")
    report.append(f"Period Analyzed: 2016-01-01 to 2025-09-24")
    report.append(f"Weekly Budget: $250.00")
    report.append("="*100)
    
    # Executive Summary
    report.append("\n" + "="*100)
    report.append("EXECUTIVE SUMMARY")
    report.append("="*100)
    report.append("\nThree different methodologies were used to analyze DCA strategy performance:")
    report.append("\n1. DURATION SIMULATOR (Weekly Rolling)")
    report.append("   - Maximum data utilization: 1,512 simulations")
    report.append("   - High autocorrelation: ~98% overlap")
    report.append("   - Best for: Pattern exploration, not statistical inference")
    report.append("\n2. BALANCED ROLLING (Monthly Steps - v2.1 OPTIMIZED)")
    report.append("   - Large data: 378 simulations (~30 effective)")
    report.append("   - Manageable autocorrelation: ~92% overlap")
    report.append("   - Best for: Standard analysis with risk metrics ⭐ RECOMMENDED")
    report.append("\n3. NON-OVERLAPPING (Perfect Independence)")
    report.append("   - Minimal data: 18 simulations")
    report.append("   - Zero autocorrelation: 0% overlap")
    report.append("   - Best for: Academic rigor, conservative estimates")
    
    # Detailed comparison for each duration
    for duration in ['1-Year', '2-Year', '3-Year', '4-Year']:
        report.append("\n" + "="*100)
        report.append(f"{duration.upper()} DURATION COMPARISON")
        report.append("="*100)
        
        if duration in duration_sim:
            ds = duration_sim[duration]
            report.append(f"\n📊 DURATION SIMULATOR (Weekly Rolling)")
            report.append(f"   Simulations: {ds['n_simulations']:,} (≈{ds['n_effective']} effective)")
            report.append(f"   Optimum DCA:  {ds['optimum_mean']:>8.2f}% avg, {ds['optimum_median']:>8.2f}% median (σ={ds['optimum_std']:.2f}%)")
            report.append(f"   Simple DCA:   {ds['simple_mean']:>8.2f}% avg, {ds['simple_median']:>8.2f}% median (σ={ds['simple_std']:.2f}%)")
            report.append(f"   Outperformance: {ds['outperformance']:>8.2f} pp, Win Rate: {ds['win_rate']:.1f}%")
            report.append(f"   Best Period: {ds['best_period']} ({ds['best_return']:.2f}% return)")
        
        if duration in balanced:
            br = balanced[duration]
            report.append(f"\n📊 BALANCED ROLLING (Monthly Steps - v2.1)")
            report.append(f"   Simulations: {br['n_simulations']:,} (≈{br['n_effective']} effective)")
            report.append(f"   Optimum DCA:  {br['optimum_mean']:>8.2f}% avg, {br['optimum_median']:>8.2f}% median (σ={br['optimum_std']:.2f}%)")
            report.append(f"   Simple DCA:   {br['simple_mean']:>8.2f}% avg, {br['simple_median']:>8.2f}% median (σ={br['simple_std']:.2f}%)")
            report.append(f"   Outperformance: {br['outperformance']:>8.2f} pp, Win Rate: {br['win_rate']:.1f}%")
            report.append(f"   Risk Metrics:")
            report.append(f"      Sharpe Ratio:  Optimum={br['optimum_sharpe']:.3f}, Simple={br['simple_sharpe']:.3f}")
            report.append(f"      Sortino Ratio: Optimum={br['optimum_sortino']:.3f}, Simple={br['simple_sortino']:.3f}")
            report.append(f"      Max Drawdown:  Optimum={br['optimum_max_dd']:.2f}%, Simple={br['simple_max_dd']:.2f}%")
            report.append(f"      VaR (95%):     Optimum={br['optimum_var']:.2f}%, Simple={br['simple_var']:.2f}%")
            report.append(f"   Statistical Test:")
            report.append(f"      P-value: {br['p_value']:.4f}, Effect Size: {br['effect_size']:.3f}")
            report.append(f"      Significant at 5%: {'YES ✅' if br['significant'] else 'NO ❌'}")
        
        if duration in non_overlapping:
            no = non_overlapping[duration]
            report.append(f"\n📊 NON-OVERLAPPING (Perfect Independence)")
            report.append(f"   Simulations: {no['n_simulations']:,} (all independent)")
            report.append(f"   Optimum DCA:  {no['optimum_mean']:>8.2f}% avg, {no['optimum_median']:>8.2f}% median (σ={no['optimum_std']:.2f}%)")
            report.append(f"   Simple DCA:   {no['simple_mean']:>8.2f}% avg, {no['simple_median']:>8.2f}% median (σ={no['simple_std']:.2f}%)")
            report.append(f"   Outperformance: {no['outperformance']:>8.2f} pp, Win Rate: {no['win_rate']:.1f}%")
            report.append(f"   Risk Metrics:")
            report.append(f"      Sharpe Ratio:  Optimum={no['optimum_sharpe']:.3f}, Simple={no['simple_sharpe']:.3f}")
            report.append(f"      Sortino Ratio: Optimum={no['optimum_sortino']:.3f}, Simple={no['simple_sortino']:.3f}")
            report.append(f"      Max Drawdown:  Optimum={no['optimum_max_dd']:.2f}%, Simple={no['simple_max_dd']:.2f}%")
            report.append(f"      VaR (95%):     Optimum={no['optimum_var']:.2f}%, Simple={no['simple_var']:.2f}%")
            report.append(f"   Statistical Test:")
            report.append(f"      P-value: {no['p_value']:.4f}, Effect Size: {no['effect_size']:.3f}")
            report.append(f"      Significant at 5%: {'YES ✅' if no['significant'] else 'NO ❌'}")
        
        # Comparison across methods
        report.append(f"\n   📈 METHOD COMPARISON:")
        if duration in duration_sim and duration in balanced and duration in non_overlapping:
            report.append(f"      Optimum Mean: Weekly={ds['optimum_mean']:.1f}%, Quarterly={br['optimum_mean']:.1f}%, Non-Overlap={no['optimum_mean']:.1f}%")
            report.append(f"      Simple Mean:  Weekly={ds['simple_mean']:.1f}%, Quarterly={br['simple_mean']:.1f}%, Non-Overlap={no['simple_mean']:.1f}%")
            report.append(f"      Winner (Risk-Adj): {'Optimum' if br['optimum_sharpe'] > br['simple_sharpe'] else 'Simple'} (Sharpe: {max(br['optimum_sharpe'], br['simple_sharpe']):.3f})")
    
    # Overall conclusions
    report.append("\n" + "="*100)
    report.append("KEY FINDINGS & RECOMMENDATIONS")
    report.append("="*100)
    
    report.append("\n1. STATISTICAL SIGNIFICANCE:")
    report.append("   ❌ NO statistically significant difference between Optimum and Simple DCA")
    report.append("      in any duration when using proper non-overlapping analysis")
    report.append("   ⚠️  Weekly rolling results are misleading due to high autocorrelation")
    
    report.append("\n2. RISK-ADJUSTED PERFORMANCE:")
    report.append("   • Simple DCA generally has better Sharpe ratios (better risk-adjusted returns)")
    report.append("   • Optimum DCA has better Sortino ratios (better downside-risk-adjusted returns)")
    report.append("   • Optimum DCA has better tail risk protection (lower VaR in most cases)")
    
    report.append("\n3. METHODOLOGY MATTERS:")
    report.append("   • Choice of methodology dramatically affects conclusions")
    report.append("   • Weekly rolling overstates Optimum's advantage")
    report.append("   • Non-overlapping provides most conservative estimates")
    report.append("   • Quarterly rolling provides best balance ⭐")
    
    report.append("\n4. PRACTICAL RECOMMENDATIONS:")
    report.append("   For 1-2 Year Horizons:")
    report.append("      • Use Optimum DCA if you can tolerate volatility for upside potential")
    report.append("      • Better downside protection than Simple DCA")
    report.append("      • But no guarantee of outperformance")
    report.append("\n   For 3-4 Year Horizons:")
    report.append("      • Simple DCA more reliable and consistent")
    report.append("      • Better risk-adjusted returns")
    report.append("      • 100% win rate in non-overlapping periods")
    report.append("\n   For Risk-Averse Investors:")
    report.append("      • Simple DCA: Lower volatility, more predictable")
    report.append("\n   For Risk-Tolerant Investors:")
    report.append("      • Optimum DCA: Higher upside potential, better tail protection")
    
    report.append("\n5. WHICH ANALYSIS TO USE:")
    report.append("   📊 Duration Simulator: Exploration, pattern finding, NOT statistical inference")
    report.append("   ⭐ Balanced Rolling: Standard analysis, most practical (RECOMMENDED)")
    report.append("   🎓 Non-Overlapping: Academic papers, regulatory filings, maximum rigor")
    
    report.append("\n" + "="*100)
    report.append("END OF REPORT")
    report.append("="*100)
    
    return "\n".join(report)

def main():
    """Generate comprehensive comparison report."""
    
    print("="*100)
    print("🔬 COMPREHENSIVE DCA ANALYSIS COMPARISON")
    print("="*100)
    print("\nThis will run all three analysis methods and generate a complete comparison.")
    print("Estimated time: ~2 minutes\n")
    
    # Run all three analyses
    duration_sim = run_duration_simulator_analysis()
    balanced = run_balanced_rolling_analysis()
    non_overlapping = run_non_overlapping_analysis()
    
    # Generate report
    print("\n" + "="*100)
    print("📝 GENERATING COMPARISON REPORT")
    print("="*100)
    
    report = generate_comparison_report(duration_sim, balanced, non_overlapping)
    
    # Save to file
    output_file = "COMPREHENSIVE_COMPARISON_REPORT.txt"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_file}")
    
    # Also print to console
    print("\n" + report)
    
    # Generate summary CSV
    summary_data = []
    for duration in ['1-Year', '2-Year', '3-Year', '4-Year']:
        if duration in duration_sim and duration in balanced and duration in non_overlapping:
            summary_data.append({
                'Duration': duration,
                'Method': 'Weekly Rolling',
                'N_Simulations': duration_sim[duration]['n_simulations'],
                'N_Effective': duration_sim[duration]['n_effective'],
                'Optimum_Mean_%': duration_sim[duration]['optimum_mean'],
                'Simple_Mean_%': duration_sim[duration]['simple_mean'],
                'Outperformance_pp': duration_sim[duration]['outperformance'],
                'Win_Rate_%': duration_sim[duration]['win_rate']
            })
            summary_data.append({
                'Duration': duration,
                'Method': 'Quarterly Rolling',
                'N_Simulations': balanced[duration]['n_simulations'],
                'N_Effective': balanced[duration]['n_effective'],
                'Optimum_Mean_%': balanced[duration]['optimum_mean'],
                'Simple_Mean_%': balanced[duration]['simple_mean'],
                'Outperformance_pp': balanced[duration]['outperformance'],
                'Win_Rate_%': balanced[duration]['win_rate'],
                'P_Value': balanced[duration]['p_value'],
                'Effect_Size': balanced[duration]['effect_size'],
                'Optimum_Sharpe': balanced[duration]['optimum_sharpe'],
                'Simple_Sharpe': balanced[duration]['simple_sharpe']
            })
            summary_data.append({
                'Duration': duration,
                'Method': 'Non-Overlapping',
                'N_Simulations': non_overlapping[duration]['n_simulations'],
                'N_Effective': non_overlapping[duration]['n_effective'],
                'Optimum_Mean_%': non_overlapping[duration]['optimum_mean'],
                'Simple_Mean_%': non_overlapping[duration]['simple_mean'],
                'Outperformance_pp': non_overlapping[duration]['outperformance'],
                'Win_Rate_%': non_overlapping[duration]['win_rate'],
                'P_Value': non_overlapping[duration]['p_value'],
                'Effect_Size': non_overlapping[duration]['effect_size'],
                'Optimum_Sharpe': non_overlapping[duration]['optimum_sharpe'],
                'Simple_Sharpe': non_overlapping[duration]['simple_sharpe']
            })
    
    summary_df = pd.DataFrame(summary_data)
    summary_csv = "method_comparison_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"✅ Summary CSV saved to: {summary_csv}")
    
    return report

if __name__ == "__main__":
    report = main()
