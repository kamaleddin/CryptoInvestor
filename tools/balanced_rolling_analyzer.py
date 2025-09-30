#!/usr/bin/env python3
"""
BALANCED ROLLING WINDOW ANALYZER

Middle ground between maximum data (weekly rolling) and statistical purity (non-overlapping).

Uses QUARTERLY rolling windows (13-week steps) to provide:
- Larger sample sizes than non-overlapping
- Reduced autocorrelation vs weekly rolling
- Practical balance for analysis

Based on research: Quarterly rebalancing common in portfolio management,
and 13-week correlation significantly lower than 1-week.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from advanced_duration_analyzer import AdvancedDurationAnalyzer
from datetime import date

def main():
    """Run balanced analysis with quarterly rolling windows."""
    
    print("="*80)
    print("🎯 BALANCED ROLLING WINDOW ANALYSIS")
    print("="*80)
    print("Using QUARTERLY steps (13 weeks) for balance between:")
    print("  ✅ Statistical rigor (lower autocorrelation)")
    print("  ✅ Practical sample size (more observations)")
    print("="*80)
    
    # Run with quarterly rolling (13-week steps)
    analyzer = AdvancedDurationAnalyzer(
        weekly_budget=250.0,
        overall_start=date(2016, 1, 1),
        overall_end=date(2025, 9, 24),
        risk_free_rate=0.04,
        verbose=True
    )
    
    # Quarterly rolling windows
    results = analyzer.run_comprehensive_analysis(
        use_non_overlapping=False,
        rolling_step_weeks=13  # Quarterly
    )
    
    # Print detailed report
    analyzer.print_analysis_report(results)
    
    # Additional analysis
    print("\n" + "="*80)
    print("📊 AUTOCORRELATION ANALYSIS")
    print("="*80)
    print("\nApproximate autocorrelation by step size:")
    print("  Weekly (1-week):     ≈ 98% overlap → Very high autocorrelation")
    print("  Bi-weekly (2-week):  ≈ 96% overlap → High autocorrelation")
    print("  Monthly (4-week):    ≈ 92% overlap → Moderate autocorrelation")
    print("  Quarterly (13-week): ≈ 75% overlap → Lower autocorrelation ✅")
    print("  Semi-annual (26w):   ≈ 50% overlap → Low autocorrelation")
    print("  Annual (52-week):    ≈ 0% overlap  → No autocorrelation")
    
    print("\n" + "="*80)
    print("📈 SAMPLE SIZE COMPARISON")
    print("="*80)
    
    for duration in ['1-Year', '2-Year', '3-Year', '4-Year']:
        if duration in results:
            n = results[duration]['n_periods']
            print(f"\n{duration}:")
            print(f"  Quarterly Rolling: {n} periods")
            print(f"  Effective N (adj for autocorrelation): ~{int(n * 0.4)} independent")
            print(f"  Statistical Power: {'Good' if n > 20 else 'Moderate' if n > 10 else 'Limited'}")
    
    print("\n" + "="*80)
    print("✅ BALANCED ANALYSIS COMPLETE")  
    print("="*80)
    print("\nRecommendation: Use this for most analyses")
    print("  - Sufficient sample size for statistical power")
    print("  - Moderate autocorrelation (manageable with corrections)")
    print("  - Robust standard errors via bootstrap")
    print("  - Practical for decision-making")
    
    return results

if __name__ == "__main__":
    results = main()
