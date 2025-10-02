#!/usr/bin/env python3
"""
 CryptoInvestor - Quick Start Example

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
    print(" Error: Could not import optimum_dca_analyzer")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def run_test_case():
    """Run the test case validation."""
    
    print(" TEST CASE VALIDATION")
    print("=" * 50)
    print("Running with test case parameters (should give 462.1% return)")
    
    # Create analyzer with test case defaults (non-verbose)
    analyzer = FlexibleOptimumDCA(verbose=False)
    
    # Run both strategies
    optimum_results = analyzer.run_optimum_dca_simulation()
    simple_results = analyzer.run_simple_dca_simulation()
    
    # Display results
    print(f"\n RESULTS:")
    print(f"Period: {analyzer.start_date} to {analyzer.end_date} | Budget: ${analyzer.weekly_budget:.0f}/week")
    
    print(f"\n OPTIMUM DCA:  {optimum_results['profit_pct']:>6.1f}% return | ${optimum_results['holding_value']:>11,.0f} value | {optimum_results['total_btc']:.8f} BTC")
    print(f" SIMPLE DCA:   {simple_results['profit_pct']:>6.1f}% return | ${simple_results['holding_value']:>11,.0f} value | {simple_results['total_btc']:.8f} BTC")
    
    # Validation
    expected_return = 462.1
    return_match = abs(optimum_results['profit_pct'] - expected_return) < 0.1
    
    print(f"\n VALIDATION: Expected {expected_return:.1f}% | Actual {optimum_results['profit_pct']:.1f}% | {' PASSED' if return_match else ' FAILED'}")
    
    return return_match

def run_custom_examples():
    """Run examples with custom date ranges."""
    
    print("\n CUSTOM DATE RANGE EXAMPLES")
    print("=" * 50)
    
    examples = [
        {
            'name': ' Bear Market 2022',
            'budget': 250.0,
            'start': date(2022, 1, 1),
            'end': date(2022, 12, 31)
        },
        {
            'name': ' Recovery 2023',
            'budget': 300.0,
            'start': date(2023, 1, 1),
            'end': date(2023, 12, 31)
        },
        {
            'name': ' Bull Run 2024 (6mo)',
            'budget': 500.0,
            'start': date(2024, 1, 1),
            'end': date(2024, 6, 30)
        }
    ]
    
    for example in examples:
        analyzer = FlexibleOptimumDCA(
            weekly_budget=example['budget'],
            start_date=example['start'],
            end_date=example['end'],
            verbose=False
        )
        
        optimum = analyzer.run_optimum_dca_simulation()
        simple = analyzer.run_simple_dca_simulation()
        
        outperformance = optimum['profit_pct'] - simple['profit_pct']
        
        print(f"\n{example['name']}")
        print(f"Period: {analyzer.start_date} to {analyzer.end_date} | Budget: ${analyzer.weekly_budget:.0f}/week")
        print(f"Optimum: {optimum['profit_pct']:+6.1f}% | Simple: {simple['profit_pct']:+6.1f}% | Outperformance: {outperformance:+5.1f}pp")

def show_usage_examples():
    """Show code examples for using the analyzer."""
    
    print("\n USAGE EXAMPLES")
    print("=" * 50)
    
    print("""
# Test case with default parameters
analyzer = FlexibleOptimumDCA(verbose=False)
results = analyzer.run_optimum_dca_simulation()

# Custom parameters
analyzer = FlexibleOptimumDCA(
    weekly_budget=100.0,
    start_date=date(2023, 1, 1),
    end_date=date(2023, 12, 31),
    verbose=False
)

# Using factory function with string dates
analyzer = create_dca_analyzer(
    weekly_budget=250.0,
    start_date="2022-06-01",
    end_date="2024-05-31",
    verbose=False
)

# Running both strategies
optimum = analyzer.run_optimum_dca_simulation()
simple = analyzer.run_simple_dca_simulation()
""")

def main():
    """Run complete quick start demonstration."""
    
    print(" CRYPTOINVESTOR - FLEXIBLE DCA QUICK START")
    print("=" * 80)
    
    # 1. Test case validation
    test_passed = run_test_case()
    
    if not test_passed:
        print("\n Test case failed! Check implementation.")
        return
    
    # 2. Custom examples
    run_custom_examples()
    
    # 3. Usage examples
    show_usage_examples()
    
    # 4. Summary
    print("\n SUMMARY")
    print("=" * 50)
    print(" Test case validation: PASSED (462.1% return)")
    print(" Custom date ranges: Working")
    print(" Flexible parameters: Supported")
    print(" Clean output: No redundancy")
    
    print(f"\n KEY FEATURES:")
    print(f"   • Configurable weekly budget and date ranges")
    print(f"   • Dynamic T2/X2 calculation from CSV data")
    print(f"   • Test case validation (462.1% return)")
    print(f"   • No hard-coded Excel constants")
    print(f"   • Professional output formatting")
    
    print(f"\n FOR MORE INFO:")
    print(f"   • Detailed analysis: docs/analysis_report.md")
    print(f"   • Excel validation: python tools/excel_validator.py")
    print(f"   • Source code: src/optimum_dca_analyzer.py")
    
    print("\n Ready to analyze your custom DCA strategies!")

if __name__ == "__main__":
    main()