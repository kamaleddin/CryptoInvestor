#!/usr/bin/env python3
"""
🚀 CryptoInvestor - Quick Start Example

This example shows how to use the Flexible Optimum DCA Analyzer with both
test case validation and custom date ranges.

Expected Test Case Results (2022-01-10 to 2025-09-22):
- Optimum DCA: 462.1% return, $263,077.09 value, 2.26483845 BTC
- Simple DCA: 209.4% return, $150,048.67 value, 1.29177345 BTC
"""

import sys
import os
from datetime import date

# Add src directory to path so we can import the analyzer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from optimum_dca_analyzer import FlexibleOptimumDCA, create_dca_analyzer
except ImportError:
    print("❌ Error: Could not import optimum_dca_analyzer")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def run_test_case():
    """Run the test case validation."""
    
    print("="*80)
    print("🧪 TEST CASE VALIDATION")
    print("="*80)
    print("Running with test case parameters (should give 462.1% return)...")
    
    # Create analyzer with test case defaults
    analyzer = FlexibleOptimumDCA()  # Uses test case defaults
    
    # Run both strategies
    optimum_results = analyzer.run_optimum_dca_simulation()
    simple_results = analyzer.run_simple_dca_simulation()
    
    # Display results
    print(f"\n📈 TEST CASE RESULTS:")
    print(f"Period: {analyzer.start_date} to {analyzer.end_date}")
    print(f"Weekly Budget: ${analyzer.weekly_budget:.2f}")
    
    print(f"\n🎯 OPTIMUM DCA:")
    print(f"   💰 Investment: ${optimum_results['total_investment']:,.2f}")
    print(f"   ₿  BTC: {optimum_results['total_btc']:.8f}")
    print(f"   💵 Value: ${optimum_results['holding_value']:,.2f}")
    print(f"   📈 Return: {optimum_results['profit_pct']:.1f}%")
    
    print(f"\n📊 SIMPLE DCA:")
    print(f"   💰 Investment: ${simple_results['total_investment']:,.2f}")
    print(f"   ₿  BTC: {simple_results['total_btc']:.8f}")
    print(f"   💵 Value: ${simple_results['holding_value']:,.2f}")
    print(f"   📈 Return: {simple_results['profit_pct']:.1f}%")
    
    # Validation
    expected_return = 462.1
    return_match = abs(optimum_results['profit_pct'] - expected_return) < 0.1
    
    print(f"\n✅ VALIDATION:")
    print(f"   Expected Return: {expected_return:.1f}%")
    print(f"   Actual Return: {optimum_results['profit_pct']:.1f}%")
    print(f"   Test Status: {'✅ PASSED' if return_match else '❌ FAILED'}")
    
    return return_match

def run_custom_examples():
    """Run examples with custom date ranges."""
    
    print("\n" + "="*80)
    print("🎯 CUSTOM DATE RANGE EXAMPLES")
    print("="*80)
    
    # Example 1: Bear Market 2022
    print("\n1. 📉 BEAR MARKET ANALYSIS (2022)")
    print("-" * 50)
    
    bear_analyzer = FlexibleOptimumDCA(
        weekly_budget=200.0,
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31)
    )
    
    bear_optimum = bear_analyzer.run_optimum_dca_simulation()
    bear_simple = bear_analyzer.run_simple_dca_simulation()
    
    print(f"Period: {bear_analyzer.start_date} to {bear_analyzer.end_date}")
    print(f"Budget: ${bear_analyzer.weekly_budget}/week")
    print(f"Optimum: {bear_optimum['profit_pct']:+.1f}% | Simple: {bear_simple['profit_pct']:+.1f}%")
    print(f"Outperformance: {bear_optimum['profit_pct'] - bear_simple['profit_pct']:+.1f} percentage points")
    
    # Example 2: Recovery 2023
    print("\n2. 📈 RECOVERY ANALYSIS (2023)")
    print("-" * 50)
    
    recovery_analyzer = create_dca_analyzer(
        weekly_budget=300.0,
        start_date="2023-01-01",
        end_date="2023-12-31"
    )
    
    recovery_optimum = recovery_analyzer.run_optimum_dca_simulation()
    recovery_simple = recovery_analyzer.run_simple_dca_simulation()
    
    print(f"Period: {recovery_analyzer.start_date} to {recovery_analyzer.end_date}")
    print(f"Budget: ${recovery_analyzer.weekly_budget}/week")
    print(f"Optimum: {recovery_optimum['profit_pct']:+.1f}% | Simple: {recovery_simple['profit_pct']:+.1f}%")
    print(f"Outperformance: {recovery_optimum['profit_pct'] - recovery_simple['profit_pct']:+.1f} percentage points")
    
    # Example 3: Short-term 2024
    print("\n3. ⚡ SHORT-TERM ANALYSIS (6 months, 2024)")
    print("-" * 50)
    
    short_analyzer = FlexibleOptimumDCA(
        weekly_budget=500.0,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 30)
    )
    
    short_optimum = short_analyzer.run_optimum_dca_simulation()
    short_simple = short_analyzer.run_simple_dca_simulation()
    
    print(f"Period: {short_analyzer.start_date} to {short_analyzer.end_date}")
    print(f"Budget: ${short_analyzer.weekly_budget}/week")
    print(f"Optimum: {short_optimum['profit_pct']:+.1f}% | Simple: {short_simple['profit_pct']:+.1f}%")
    print(f"Outperformance: {short_optimum['profit_pct'] - short_simple['profit_pct']:+.1f} percentage points")

def show_usage_examples():
    """Show code examples for using the analyzer."""
    
    print("\n" + "="*80)
    print("💻 USAGE EXAMPLES")
    print("="*80)
    
    print("""
# Example 1: Test case (default parameters)
analyzer = FlexibleOptimumDCA()
results = analyzer.run_optimum_dca_simulation()

# Example 2: Custom parameters
analyzer = FlexibleOptimumDCA(
    weekly_budget=100.0,
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31)
)

# Example 3: Using factory function with string dates
analyzer = create_dca_analyzer(
    weekly_budget=250.0,
    start_date="2022-06-01",
    end_date="2024-05-31",
    final_btc_price=70000.0
)

# Example 4: Running validation
test_passed = analyzer.run_test_validation()
""")

def main():
    """Run complete quick start demonstration."""
    
    print("="*80)
    print("🚀 CRYPTOINVESTOR - FLEXIBLE DCA QUICK START")
    print("="*80)
    
    # 1. Test case validation
    test_passed = run_test_case()
    
    if not test_passed:
        print("\n❌ Test case failed! Check implementation.")
        return
    
    # 2. Custom examples
    run_custom_examples()
    
    # 3. Usage examples
    show_usage_examples()
    
    # 4. Summary
    print("\n" + "="*80)
    print("📚 SUMMARY")
    print("="*80)
    print("✅ Test case validation: PASSED (462.1% return)")
    print("✅ Custom date ranges: Working")
    print("✅ Flexible parameters: Supported")
    print("✅ Factory function: Available")
    
    print(f"\n🎯 KEY FEATURES:")
    print(f"   • Configurable weekly budget")
    print(f"   • Custom start/end dates")
    print(f"   • Test case validation")
    print(f"   • Dynamic T2/X2 calculation")
    print(f"   • No hard-coded Excel constants")
    
    print(f"\n📖 FOR MORE INFO:")
    print(f"   • Detailed analysis: docs/analysis_report.md")
    print(f"   • Excel validation: python tools/excel_validator.py")
    print(f"   • Custom testing: python test_custom_dates.py")
    
    print("\n🎉 Ready to analyze your custom DCA strategies!")

if __name__ == "__main__":
    main()
