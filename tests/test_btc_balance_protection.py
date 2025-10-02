#!/usr/bin/env python3
"""
Test suite to ensure Optimum DCA never allows negative BTC holdings.
This prevents the critical bug where the strategy would sell more BTC than owned.
"""

import sys
import os
from datetime import date
import pytest

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from optimum_dca_analyzer import FlexibleOptimumDCA

def test_no_negative_btc_during_bull_market():
    """Test that BTC balance never goes negative during a bull market (2023-2024)."""
    analyzer = FlexibleOptimumDCA(
        weekly_budget=300.0,
        start_date=date(2023, 1, 1),
        end_date=date(2024, 12, 31),
        verbose=False
    )

    results = analyzer.run_optimum_dca_simulation()

    # Check that final BTC is not negative
    assert results['total_btc'] >= 0, f"Final BTC balance is negative: {results['total_btc']}"

    # Check that no intermediate balance was negative
    min_balance = float('inf')
    for week_result in results['weekly_results']:
        if 'btc_balance' in week_result:
            min_balance = min(min_balance, week_result['btc_balance'])
            assert week_result['btc_balance'] >= -1e-10, f"Negative BTC balance on {week_result['date']}: {week_result['btc_balance']}"

    # Verify we actually checked some balances
    assert min_balance < float('inf'), "No BTC balances were tracked"

    print(f" Bull market test passed - Min balance: {min_balance:.8f} BTC, Final: {results['total_btc']:.8f} BTC")

def test_no_negative_btc_short_bull_run():
    """Test that BTC balance never goes negative during short bull run (2024 H1)."""
    analyzer = FlexibleOptimumDCA(
        weekly_budget=500.0,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 6, 30),
        verbose=False
    )

    results = analyzer.run_optimum_dca_simulation()

    # Check that final BTC is not negative
    assert results['total_btc'] >= 0, f"Final BTC balance is negative: {results['total_btc']}"

    # Check cumulative balance throughout
    for week_result in results['weekly_results']:
        if 'btc_balance' in week_result:
            assert week_result['btc_balance'] >= -1e-10, f"Negative BTC balance on {week_result['date']}: {week_result['btc_balance']}"

    print(f" Short bull run test passed - Final BTC: {results['total_btc']:.8f}")

def test_balance_consistency():
    """Test that the final total_btc matches the last btc_balance."""
    analyzer = FlexibleOptimumDCA(
        weekly_budget=250.0,
        start_date=date(2022, 1, 1),
        end_date=date(2023, 12, 31),
        verbose=False
    )

    results = analyzer.run_optimum_dca_simulation()

    if results['weekly_results'] and 'btc_balance' in results['weekly_results'][-1]:
        last_balance = results['weekly_results'][-1]['btc_balance']
        total_btc = results['total_btc']

        # Allow small floating point difference
        assert abs(last_balance - total_btc) < 1e-10, \
            f"Inconsistent BTC tracking: last_balance={last_balance}, total_btc={total_btc}"

    print(f" Balance consistency test passed")

def test_sell_limitation():
    """Test that selling is limited to available BTC balance."""
    # Start from a period likely to trigger sells
    analyzer = FlexibleOptimumDCA(
        weekly_budget=100.0,
        start_date=date(2024, 3, 1),  # Start during high prices
        end_date=date(2024, 4, 30),
        verbose=False
    )

    results = analyzer.run_optimum_dca_simulation()

    # Track cumulative purchased vs sold
    total_bought = 0.0
    total_sold = 0.0

    for week_result in results['weekly_results']:
        btc_change = week_result['btc_purchased']
        if btc_change > 0:
            total_bought += btc_change
        else:
            total_sold += abs(btc_change)

    # Cannot sell more than bought
    assert total_sold <= total_bought + 1e-10, \
        f"Sold more than bought: sold={total_sold:.8f}, bought={total_bought:.8f}"

    print(f" Sell limitation test passed - Bought: {total_bought:.8f}, Sold: {total_sold:.8f}")

def test_original_test_case_still_works():
    """Ensure the fix doesn't break the original test case."""
    analyzer = FlexibleOptimumDCA(verbose=False)  # Uses default test case dates

    results = analyzer.run_optimum_dca_simulation()

    # Original test case should still achieve roughly 462% return
    # Allow some tolerance due to the balance protection
    assert results['profit_pct'] > 450, f"Test case return too low: {results['profit_pct']:.1f}%"
    assert results['profit_pct'] < 470, f"Test case return too high: {results['profit_pct']:.1f}%"

    print(f" Original test case still works - Return: {results['profit_pct']:.1f}%")

if __name__ == "__main__":
    print(" Running BTC Balance Protection Tests")
    print("=" * 60)

    test_no_negative_btc_during_bull_market()
    test_no_negative_btc_short_bull_run()
    test_balance_consistency()
    test_sell_limitation()
    test_original_test_case_still_works()

    print("\n All BTC balance protection tests passed!")
    print("The strategy now correctly prevents selling more BTC than owned.")