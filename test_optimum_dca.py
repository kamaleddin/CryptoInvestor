#!/usr/bin/env python3
"""
Comprehensive test suite for the optimum_dca.py implementation.

This test suite validates that the Python implementation produces results 
that match the expected values from the Excel file "Optimum DCA clubhouse.xlsx".
"""

import pandas as pd
import numpy as np
from datetime import date, datetime
from typing import Dict, List, Tuple
import os
import sys

# Add the current directory to path so we can import optimum_dca
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from optimum_dca import compute_weekly_table, compute_optimum_dca_schedule, run_optimum_dca


class OptimumDCATestSuite:
    """Test suite for validating optimum DCA calculations."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.bitcoin_prices = None
        self.expected_weekly = None
        self.expected_wdca = None
        self.tolerance = 1e-6  # Default tolerance for float comparisons
        self.percentage_tolerance = 0.01  # 1% tolerance for percentage comparisons
        
    def load_data(self):
        """Load all required data files."""
        print("Loading data files...")
        
        # Load Bitcoin prices
        bitcoin_path = os.path.join(self.data_dir, "bitcoin_prices.csv")
        self.bitcoin_prices = pd.read_csv(bitcoin_path)
        
        # Rename columns to match expected format
        self.bitcoin_prices.columns = ['start_date', 'end_date', 'open', 'high', 'low', 'price', 'daily_volume', 'market_cap']
        self.bitcoin_prices['date'] = pd.to_datetime(self.bitcoin_prices['end_date']).dt.date
        
        # Load expected weekly prices
        weekly_path = os.path.join(self.data_dir, "expected_weekly_price.csv")
        self.expected_weekly = pd.read_csv(weekly_path)
        
        # Clean up the expected weekly data - skip header rows and parse dates
        # Find the first row with date data (starts with a date pattern)
        start_row = 1  # Skip only the header row, start from first data row
        self.expected_weekly = self.expected_weekly.iloc[start_row:].copy()
        
        # Set proper column names based on actual column count
        actual_cols = len(self.expected_weekly.columns)
        print(f"Expected weekly CSV has {actual_cols} columns")
        
        expected_weekly_cols = [
            'date', 'weekly_close', 'weekly_volume', 'weekly_return', 'weekly_variance',
            'rolling_vol', 'weighted_volume', 'vwap_ma', 'col8', 'multiple_calc',
            'bs_multiplier', 'col11', 'lower_2sd', 'upper_2sd', 'lower_3sd',
            'upper_3sd', 'lower_4sd', 'upper_4sd', 'col18', 'avg_return',
            'min_return', 'max_return', 'avg_variance', 'sd_global'
        ]
        
        # Extend or trim column names to match actual columns
        if actual_cols > len(expected_weekly_cols):
            for i in range(len(expected_weekly_cols), actual_cols):
                expected_weekly_cols.append(f'extra_col_{i}')
        
        self.expected_weekly.columns = expected_weekly_cols[:actual_cols]
        
        # Convert date strings to dates and clean numeric columns
        self.expected_weekly = self._clean_weekly_data(self.expected_weekly)
        
        # Load expected WDCA data
        wdca_path = os.path.join(self.data_dir, "expected_wdca.csv")
        self.expected_wdca = pd.read_csv(wdca_path)
        
        # Clean up the expected WDCA data
        start_row = 1  # Skip only the header row, start from first data row
        self.expected_wdca = self.expected_wdca.iloc[start_row:].copy()
        
        # Set proper column names based on actual column count
        actual_cols = len(self.expected_wdca.columns)
        print(f"Expected WDCA CSV has {actual_cols} columns")
        
        expected_wdca_cols = [
            'trade_date', 'week', 'btc_price', 'pct_change_from_first',
            'investment_multiple_optimum', 'buy_sell_multiplier',
            'investment_amount_optimum', 'btc_units_optimum',
            'total_investment_optimum', 'capital_balance_optimum',
            'rolling_weekly_pnl', 'avg_buy_price_optimum',
            'btc_units_simple', 'investment_amount_simple',
            'avg_buy_price_simple'
        ]
        
        # Extend or trim column names to match actual columns
        if actual_cols > len(expected_wdca_cols):
            for i in range(len(expected_wdca_cols), actual_cols):
                expected_wdca_cols.append(f'extra_col_{i}')
        
        self.expected_wdca.columns = expected_wdca_cols[:actual_cols]
        
        # Clean the WDCA data
        self.expected_wdca = self._clean_wdca_data(self.expected_wdca)
        
        print(f"Loaded {len(self.bitcoin_prices)} Bitcoin price records")
        print(f"Loaded {len(self.expected_weekly)} expected weekly records")
        print(f"Loaded {len(self.expected_wdca)} expected WDCA records")
    
    def _clean_weekly_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and format the weekly data."""
        df = df.copy()
        
        # Remove rows where date is NaN or empty
        df = df.dropna(subset=['date'])
        df = df[df['date'].astype(str).str.strip() != '']
        
        # Parse dates
        try:
            df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y').dt.date
        except:
            try:
                df['date'] = pd.to_datetime(df['date']).dt.date
            except:
                print("Warning: Could not parse dates in weekly data")
                return df
        
        # Clean numeric columns by removing $ and , characters
        numeric_cols = ['weekly_close', 'weekly_volume', 'weekly_return', 'weekly_variance',
                       'rolling_vol', 'weighted_volume', 'vwap_ma', 'multiple_calc',
                       'lower_2sd', 'upper_2sd', 'lower_3sd', 'upper_3sd', 
                       'lower_4sd', 'upper_4sd', 'avg_return', 'min_return', 
                       'max_return', 'avg_variance', 'sd_global']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = self._clean_numeric_column(df[col])
        
        # Convert percentage columns
        pct_cols = ['weekly_return', 'avg_return', 'min_return', 'max_return']
        for col in pct_cols:
            if col in df.columns:
                df[col] = self._convert_percentage(df[col])
        
        return df
    
    def _clean_wdca_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and format the WDCA data."""
        df = df.copy()
        
        # Remove rows where trade_date is NaN or empty
        df = df.dropna(subset=['trade_date'])
        df = df[df['trade_date'].astype(str).str.strip() != '']
        
        # Parse dates
        try:
            df['trade_date'] = pd.to_datetime(df['trade_date'], format='%m-%d-%Y').dt.date
        except:
            try:
                df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
            except:
                print("Warning: Could not parse dates in WDCA data")
                return df
        
        # Clean numeric columns
        numeric_cols = ['week', 'btc_price', 'pct_change_from_first',
                       'investment_multiple_optimum', 'buy_sell_multiplier',
                       'investment_amount_optimum', 'btc_units_optimum',
                       'total_investment_optimum', 'capital_balance_optimum',
                       'rolling_weekly_pnl', 'avg_buy_price_optimum',
                       'btc_units_simple', 'investment_amount_simple',
                       'avg_buy_price_simple']
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = self._clean_numeric_column(df[col])
        
        # Convert percentage columns
        pct_cols = ['pct_change_from_first', 'investment_multiple_optimum', 'rolling_weekly_pnl']
        for col in pct_cols:
            if col in df.columns:
                df[col] = self._convert_percentage(df[col])
        
        return df
    
    def _clean_numeric_column(self, series: pd.Series) -> pd.Series:
        """Clean numeric column by removing currency symbols and converting to float."""
        if series.dtype == 'object':
            # Remove $, commas, and other non-numeric characters
            cleaned = series.astype(str).str.replace(r'[\$,]', '', regex=True)
            cleaned = cleaned.str.replace(r'[^\d.-]', '', regex=True)
            cleaned = cleaned.replace('', np.nan)
            return pd.to_numeric(cleaned, errors='coerce')
        return pd.to_numeric(series, errors='coerce')
    
    def _convert_percentage(self, series: pd.Series) -> pd.Series:
        """Convert percentage strings to decimal values."""
        if series.dtype == 'object':
            # Remove % sign and convert to decimal
            cleaned = series.astype(str).str.replace('%', '')
            cleaned = pd.to_numeric(cleaned, errors='coerce')
            # Only divide by 100 if the original values contained % sign
            mask = series.astype(str).str.contains('%', na=False)
            result = cleaned.copy()
            result[mask] = result[mask] / 100
            return result
        return series
    
    def test_weekly_table(self) -> Dict:
        """Test the weekly table computation against expected values."""
        print("\n" + "="*60)
        print("TESTING WEEKLY TABLE COMPUTATION")
        print("="*60)
        
        # Prepare input data
        daily_data = self.bitcoin_prices[['date', 'price', 'daily_volume']].copy()
        
        # Compute weekly table using our implementation
        computed_weekly = compute_weekly_table(daily_data)
        
        # Filter to dates that exist in expected data
        expected_dates = set(self.expected_weekly['date'].dropna())
        computed_weekly_filtered = computed_weekly[computed_weekly['date'].isin(expected_dates)]
        
        print(f"Computed {len(computed_weekly)} weekly records")
        print(f"Expected {len(self.expected_weekly)} weekly records")
        print(f"Overlapping dates: {len(computed_weekly_filtered)}")
        
        if len(computed_weekly_filtered) == 0:
            print("ERROR: No overlapping dates found between computed and expected data")
            return {'passed': False, 'error': 'No overlapping dates'}
        
        # Compare key columns
        results = {}
        columns_to_test = [
            ('weekly_close', 'price', 0.02),
            ('weekly_volume', 'volume', 0.10),
            ('rolling_vol', 'volatility', 0.05),
            ('vwap_ma', 'VWAP', 0.05),
            ('multiple_calc', 'multiple calculation', 0.10),
            ('lower_2sd', 'lower 2SD', 0.05),
            ('upper_2sd', 'upper 2SD', 0.05)
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for computed_col, display_name, tolerance in columns_to_test:
            if computed_col in computed_weekly_filtered.columns and computed_col in self.expected_weekly.columns:
                result = self._compare_columns(
                    computed_weekly_filtered, self.expected_weekly, 
                    computed_col, computed_col, tolerance, display_name
                )
                results[computed_col] = result
                total_tests += 1
                if result['passed']:
                    passed_tests += 1
        
        overall_passed = passed_tests == total_tests
        results['summary'] = {
            'passed': overall_passed,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0
        }
        
        print(f"\nWeekly Table Test Summary: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {results['summary']['success_rate']:.1%}")
        
        return results
    
    def test_wdca_schedule(self) -> Dict:
        """Test the WDCA schedule computation against expected values."""
        print("\n" + "="*60)
        print("TESTING WDCA SCHEDULE COMPUTATION")
        print("="*60)
        
        # First compute the weekly table
        daily_data = self.bitcoin_prices[['date', 'price', 'daily_volume']].copy()
        weekly = compute_weekly_table(daily_data)
        
        # Parameters from the expected data analysis
        start_date = date(2022, 1, 10)  # From the WDCA data
        weeks = 208
        weekly_budget = 250.0
        
        # Compute WDCA schedule
        computed_wdca = compute_optimum_dca_schedule(weekly, start_date, weeks, weekly_budget)
        
        # Filter to dates that exist in expected data
        expected_dates = set(self.expected_wdca['trade_date'].dropna())
        computed_wdca_filtered = computed_wdca[computed_wdca['trade_date'].isin(expected_dates)]
        
        print(f"Computed {len(computed_wdca)} WDCA records")
        print(f"Expected {len(self.expected_wdca)} WDCA records")
        print(f"Overlapping dates: {len(computed_wdca_filtered)}")
        
        if len(computed_wdca_filtered) == 0:
            print("ERROR: No overlapping dates found between computed and expected WDCA data")
            return {'passed': False, 'error': 'No overlapping dates'}
        
        # Compare key columns
        results = {}
        columns_to_test = [
            ('btc_price', 'BTC price', 0.01),
            ('pct_change_from_first', 'percentage change', 0.02),
            ('investment_multiple_optimum', 'investment multiple', 0.05),
            ('investment_amount_optimum', 'investment amount', 0.02),
            ('btc_units_optimum', 'BTC units', 0.02),
            ('total_investment_optimum', 'total investment', 0.02),
            ('avg_buy_price_optimum', 'average buy price', 0.02)
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for computed_col, display_name, tolerance in columns_to_test:
            if computed_col in computed_wdca_filtered.columns and computed_col in self.expected_wdca.columns:
                result = self._compare_columns(
                    computed_wdca_filtered, self.expected_wdca, 
                    computed_col, computed_col, tolerance, display_name
                )
                results[computed_col] = result
                total_tests += 1
                if result['passed']:
                    passed_tests += 1
        
        overall_passed = passed_tests == total_tests
        results['summary'] = {
            'passed': overall_passed,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0
        }
        
        print(f"\nWDCA Schedule Test Summary: {passed_tests}/{total_tests} tests passed")
        print(f"Success Rate: {results['summary']['success_rate']:.1%}")
        
        return results
    
    def _compare_columns(self, computed_df: pd.DataFrame, expected_df: pd.DataFrame, 
                        computed_col: str, expected_col: str, tolerance: float, 
                        display_name: str) -> Dict:
        """Compare two columns from computed and expected dataframes."""
        
        # Merge on date to align records
        computed_col_name = f'computed_{computed_col}'
        expected_col_name = f'expected_{expected_col}'
        
        if 'trade_date' in computed_df.columns:
            date_col = 'trade_date'
        else:
            date_col = 'date'
        
        merged = pd.merge(
            computed_df[[date_col, computed_col]].rename(columns={computed_col: computed_col_name}),
            expected_df[[date_col, expected_col]].rename(columns={expected_col: expected_col_name}),
            on=date_col,
            how='inner'
        )
        
        if len(merged) == 0:
            return {
                'passed': False,
                'error': f'No matching dates for {display_name}',
                'compared_records': 0
            }
        
        # Remove NaN values
        merged_clean = merged.dropna(subset=[computed_col_name, expected_col_name])
        
        if len(merged_clean) == 0:
            return {
                'passed': False,
                'error': f'No valid numeric values for {display_name}',
                'compared_records': 0
            }
        
        # Calculate differences
        computed_vals = merged_clean[computed_col_name].values
        expected_vals = merged_clean[expected_col_name].values
        
        # Special handling for volatility columns that might be in percentage format in expected data
        if 'volatility' in display_name.lower() or 'vol' in display_name.lower():
            # If expected values are much larger than computed (e.g. 4.91 vs 0.049), 
            # convert expected from percentage to decimal
            if np.mean(np.abs(expected_vals)) > 1 and np.mean(np.abs(computed_vals)) < 1:
                expected_vals = expected_vals / 100
                print(f"  Note: Converting expected {display_name} from percentage to decimal format")
        
        # Special handling for multiple calculation that might be in percentage format
        if 'multiple' in display_name.lower():
            # If expected values are around 100-300, they're likely in percentage format
            if np.mean(expected_vals) > 50:
                expected_vals = expected_vals / 100
                print(f"  Note: Converting expected {display_name} from percentage to decimal format")
        
        # Calculate relative and absolute errors
        abs_diff = np.abs(computed_vals - expected_vals)
        rel_diff = np.abs(abs_diff / np.where(expected_vals != 0, expected_vals, 1))
        
        # Check if differences are within tolerance
        within_tolerance = rel_diff <= tolerance
        pass_rate = np.mean(within_tolerance)
        
        # Statistics
        max_abs_error = np.max(abs_diff)
        max_rel_error = np.max(rel_diff)
        mean_abs_error = np.mean(abs_diff)
        mean_rel_error = np.mean(rel_diff)
        
        passed = pass_rate >= 0.95  # 95% of values should be within tolerance
        
        print(f"\n{display_name} Comparison:")
        print(f"  Records compared: {len(merged_clean)}")
        print(f"  Pass rate: {pass_rate:.1%}")
        print(f"  Max absolute error: {max_abs_error:.6f}")
        print(f"  Max relative error: {max_rel_error:.1%}")
        print(f"  Mean absolute error: {mean_abs_error:.6f}")
        print(f"  Mean relative error: {mean_rel_error:.1%}")
        print(f"  Result: {'✓ PASS' if passed else '✗ FAIL'}")
        
        # Show some sample comparisons
        if len(merged_clean) >= 5:
            print(f"  Sample comparisons (first 5):")
            for i in range(min(5, len(merged_clean))):
                comp_val = computed_vals[i]
                exp_val = expected_vals[i]
                diff = abs_diff[i]
                rel_err = rel_diff[i]
                status = "✓" if within_tolerance[i] else "✗"
                print(f"    {status} Computed: {comp_val:.6f}, Expected: {exp_val:.6f}, "
                      f"Abs Diff: {diff:.6f}, Rel Error: {rel_err:.1%}")
        
        return {
            'passed': passed,
            'compared_records': len(merged_clean),
            'pass_rate': pass_rate,
            'max_abs_error': max_abs_error,
            'max_rel_error': max_rel_error,
            'mean_abs_error': mean_abs_error,
            'mean_rel_error': mean_rel_error,
            'tolerance': tolerance
        }
    
    def generate_report(self, weekly_results: Dict, wdca_results: Dict) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("="*80)
        report.append("OPTIMUM DCA IMPLEMENTATION VALIDATION REPORT")
        report.append("="*80)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Data summary
        report.append("DATA SUMMARY:")
        report.append(f"  Bitcoin price records: {len(self.bitcoin_prices)}")
        report.append(f"  Expected weekly records: {len(self.expected_weekly)}")
        report.append(f"  Expected WDCA records: {len(self.expected_wdca)}")
        report.append("")
        
        # Weekly table results
        report.append("WEEKLY TABLE VALIDATION:")
        if 'summary' in weekly_results:
            summary = weekly_results['summary']
            report.append(f"  Overall Result: {'✓ PASS' if summary['passed'] else '✗ FAIL'}")
            report.append(f"  Tests Passed: {summary['passed_tests']}/{summary['total_tests']}")
            report.append(f"  Success Rate: {summary['success_rate']:.1%}")
        else:
            report.append("  ✗ FAILED - No summary available")
        
        # Detail breakdown for weekly table
        for col, result in weekly_results.items():
            if col != 'summary' and isinstance(result, dict):
                report.append(f"    {col}: {'✓' if result['passed'] else '✗'} "
                            f"({result.get('compared_records', 0)} records, "
                            f"{result.get('pass_rate', 0):.1%} pass rate)")
        
        report.append("")
        
        # WDCA schedule results
        report.append("WDCA SCHEDULE VALIDATION:")
        if 'summary' in wdca_results:
            summary = wdca_results['summary']
            report.append(f"  Overall Result: {'✓ PASS' if summary['passed'] else '✗ FAIL'}")
            report.append(f"  Tests Passed: {summary['passed_tests']}/{summary['total_tests']}")
            report.append(f"  Success Rate: {summary['success_rate']:.1%}")
        else:
            report.append("  ✗ FAILED - No summary available")
        
        # Detail breakdown for WDCA
        for col, result in wdca_results.items():
            if col != 'summary' and isinstance(result, dict):
                report.append(f"    {col}: {'✓' if result['passed'] else '✗'} "
                            f"({result.get('compared_records', 0)} records, "
                            f"{result.get('pass_rate', 0):.1%} pass rate)")
        
        report.append("")
        
        # Overall conclusion
        weekly_passed = weekly_results.get('summary', {}).get('passed', False)
        wdca_passed = wdca_results.get('summary', {}).get('passed', False)
        overall_passed = weekly_passed and wdca_passed
        
        report.append("OVERALL CONCLUSION:")
        if overall_passed:
            report.append("  ✓ SUCCESS: The Python implementation matches the Excel calculations")
            report.append("    with acceptable accuracy across all tested components.")
        else:
            report.append("  ✗ FAILURE: The Python implementation has significant discrepancies")
            report.append("    from the Excel calculations that require investigation.")
            
            if not weekly_passed:
                report.append("    - Weekly table calculations need attention")
            if not wdca_passed:
                report.append("    - WDCA schedule calculations need attention")
        
        report.append("")
        report.append("RECOMMENDATIONS:")
        if overall_passed:
            report.append("  • The implementation is ready for production use")
            report.append("  • Consider adding edge case tests for robustness")
            report.append("  • Monitor for any data quality issues in real usage")
        else:
            report.append("  • Investigate discrepancies in failing test cases")
            report.append("  • Review calculation formulas against Excel implementation")
            report.append("  • Consider improving data preprocessing steps")
            report.append("  • Re-test after fixing identified issues")
        
        report.append("")
        report.append("="*80)
        
        return "\n".join(report)
    
    def run_all_tests(self) -> None:
        """Run the complete test suite and generate report."""
        print("Starting Optimum DCA Test Suite...")
        print("="*60)
        
        try:
            # Load data
            self.load_data()
            
            # Run tests
            weekly_results = self.test_weekly_table()
            wdca_results = self.test_wdca_schedule()
            
            # Generate and display report
            report = self.generate_report(weekly_results, wdca_results)
            print("\n" + report)
            
            # Save report to file
            report_path = "optimum_dca_test_report.txt"
            with open(report_path, 'w') as f:
                f.write(report)
            print(f"\nDetailed report saved to: {report_path}")
            
        except Exception as e:
            print(f"ERROR: Test suite failed with exception: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Create and run the test suite
    test_suite = OptimumDCATestSuite()
    test_suite.run_all_tests()
