#!/usr/bin/env python3
"""
🚀 CryptoInvestor - Quick Start Example

This example shows how to use the Optimum DCA Analyzer to run investment strategy analysis.

Expected Results:
- Optimum DCA: 462.1% return, $263,077.09 value, 2.26483845 BTC
- Simple DCA: 209.4% return, $150,048.67 value, 1.29177345 BTC
"""

import sys
import os

# Add src directory to path so we can import the analyzer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from optimum_dca_analyzer import CalibratedStandaloneOptimumDCA
except ImportError:
    print("❌ Error: Could not import optimum_dca_analyzer")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def main():
    """Run a quick analysis example."""
    
    print("="*80)
    print("🚀 CRYPTOINVESTOR - QUICK START EXAMPLE")
    print("="*80)
    print("Running Optimum DCA vs Simple DCA analysis...")
    print()
    
    # Initialize the analyzer
    analyzer = CalibratedStandaloneOptimumDCA(
        weekly_budget=250.0,  # $250 per week
    )
    
    # Run both strategies
    print("📊 Running analysis...")
    optimum_results = analyzer.run_optimum_dca_simulation()
    simple_results = analyzer.run_simple_dca_simulation()
    
    # Display results
    print("\n" + "="*60)
    print("📈 RESULTS SUMMARY")
    print("="*60)
    
    print(f"\n🎯 OPTIMUM DCA STRATEGY:")
    print(f"   💰 Total Investment: ${optimum_results['total_investment']:,.2f}")
    print(f"   ₿  Total BTC: {optimum_results['total_btc']:.8f}")
    print(f"   💵 Final Value: ${optimum_results['holding_value']:,.2f}")
    print(f"   📈 Return: {optimum_results['profit_pct']:.1f}%")
    
    print(f"\n📊 SIMPLE DCA STRATEGY:")
    print(f"   💰 Total Investment: ${simple_results['total_investment']:,.2f}")
    print(f"   ₿  Total BTC: {simple_results['total_btc']:.8f}")
    print(f"   💵 Final Value: ${simple_results['holding_value']:,.2f}")
    print(f"   📈 Return: {simple_results['profit_pct']:.1f}%")
    
    # Performance comparison
    outperformance = optimum_results['profit_pct'] - simple_results['profit_pct']
    print(f"\n🏆 PERFORMANCE COMPARISON:")
    print(f"   Optimum DCA outperformed Simple DCA by {outperformance:.1f} percentage points")
    print(f"   That's {optimum_results['profit_pct'] / simple_results['profit_pct']:.1f}x better returns!")
    
    # Success indicators
    expected_optimum_return = 462.1
    expected_simple_return = 209.4
    
    optimum_match = abs(optimum_results['profit_pct'] - expected_optimum_return) < 0.1
    simple_match = abs(simple_results['profit_pct'] - expected_simple_return) < 0.1
    
    print(f"\n✅ VALIDATION:")
    print(f"   Optimum DCA: {'✅ PERFECT' if optimum_match else '❌ MISMATCH'}")
    print(f"   Simple DCA: {'✅ PERFECT' if simple_match else '❌ MISMATCH'}")
    
    if optimum_match and simple_match:
        print(f"\n🎉 SUCCESS! Results match expected Excel values perfectly.")
    else:
        print(f"\n⚠️  WARNING: Results don't match expected values. Check implementation.")
    
    print("\n" + "="*60)
    print("📚 For more details, see docs/analysis_report.md")
    print("🔧 To validate against Excel, run: python tools/excel_validator.py")
    print("="*60)

if __name__ == "__main__":
    main()
