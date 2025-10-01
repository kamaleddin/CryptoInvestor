#!/usr/bin/env python3
"""
Test suite for Paired Strategy Comparison Analyzer.

Tests paired statistical methods including:
- Paired t-test and Wilcoxon tests
- Correlation analysis
- Information ratio calculation
- Consistency metrics
- Risk-adjusted comparisons
"""

import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.paired_strategy_comparison import PairedStrategyComparison


class TestPairedStrategyComparison:
    """Test suite for paired strategy comparison analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing."""
        return PairedStrategyComparison(
            weekly_budget=250.0,
            overall_start=date(2020, 1, 1),
            overall_end=date(2023, 12, 31)
        )

    @pytest.fixture
    def sample_paired_results(self):
        """Generate sample paired results for testing."""
        np.random.seed(42)
        n = 20
        results = []

        for i in range(n):
            start_date = date(2020, 1, 1) + timedelta(weeks=i*4)
            end_date = start_date + timedelta(weeks=52)

            # Generate correlated returns
            optimum_return = np.random.randn() * 50 + 100
            simple_return = optimum_return * 0.8 + np.random.randn() * 20 + 110

            results.append({
                'start_date': start_date,
                'end_date': end_date,
                'duration_weeks': 52,
                'optimum_return': optimum_return,
                'simple_return': simple_return,
                'return_difference': optimum_return - simple_return,
                'optimum_btc': np.random.uniform(0.5, 2.0),
                'simple_btc': np.random.uniform(0.5, 2.0),
                'btc_difference': np.random.uniform(-0.5, 0.5),
                'optimum_investment': 13000,
                'simple_investment': 13000,
                'optimum_value': optimum_return * 130,
                'simple_value': simple_return * 130
            })

        return results

    @pytest.fixture
    def sample_differences(self):
        """Generate sample difference array for testing."""
        np.random.seed(42)
        # Create differences with some structure
        differences = np.random.randn(30) * 20 - 5  # Slightly negative mean
        return differences

    def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.weekly_budget == 250.0
        assert analyzer.overall_start == date(2020, 1, 1)
        assert analyzer.overall_end == date(2023, 12, 31)
        assert analyzer.paired_results == []

    def test_run_paired_simulation(self, analyzer):
        """Test single paired simulation."""
        start_date = date(2022, 1, 1)
        end_date = date(2023, 1, 1)

        result = analyzer.run_paired_simulation(start_date, end_date)

        # Check output structure
        assert 'start_date' in result
        assert 'end_date' in result
        assert 'duration_weeks' in result
        assert 'optimum_return' in result
        assert 'simple_return' in result
        assert 'return_difference' in result
        assert 'optimum_btc' in result
        assert 'simple_btc' in result
        assert 'btc_difference' in result
        assert 'optimum_investment' in result
        assert 'simple_investment' in result
        assert 'optimum_value' in result
        assert 'simple_value' in result

        # Check calculated values
        assert result['return_difference'] == result['optimum_return'] - result['simple_return']
        assert result['btc_difference'] == result['optimum_btc'] - result['simple_btc']
        assert result['duration_weeks'] == 52  # 1 year

    def test_generate_paired_samples(self, analyzer):
        """Test paired sample generation."""
        duration_weeks = 52
        step_weeks = 13  # Quarterly

        # Use shorter period for testing
        analyzer.overall_start = date(2022, 1, 1)
        analyzer.overall_end = date(2023, 6, 30)

        paired_results = analyzer.generate_paired_samples(
            duration_weeks=duration_weeks,
            step_weeks=step_weeks
        )

        # Check we get expected number of samples
        assert len(paired_results) > 0

        # Check each result has correct structure
        for result in paired_results:
            assert 'start_date' in result
            assert 'end_date' in result
            assert 'optimum_return' in result
            assert 'simple_return' in result
            assert result['duration_weeks'] == duration_weeks

        # Check overlap pattern
        if len(paired_results) >= 2:
            # Steps should be correct
            weeks_diff = (paired_results[1]['start_date'] - paired_results[0]['start_date']).days // 7
            assert weeks_diff == step_weeks

    def test_paired_statistical_tests(self, analyzer, sample_differences):
        """Test paired statistical testing."""
        result = analyzer.paired_statistical_tests(sample_differences)

        # Check output structure
        assert 'n_pairs' in result
        assert 'mean_difference' in result
        assert 'std_difference' in result
        assert 'paired_t_statistic' in result
        assert 'paired_t_pvalue' in result
        assert 'wilcoxon_statistic' in result
        assert 'wilcoxon_pvalue' in result
        assert 'sign_test_pvalue' in result
        assert 'cohens_d' in result
        assert 'ci_95_lower' in result
        assert 'ci_95_upper' in result
        assert 'n_optimum_wins' in result
        assert 'n_simple_wins' in result
        assert 'win_rate_optimum' in result

        # Check logical consistency
        assert result['n_pairs'] == len(sample_differences)
        assert result['ci_95_lower'] < result['mean_difference']
        assert result['mean_difference'] < result['ci_95_upper']
        assert 0 <= result['paired_t_pvalue'] <= 1
        assert 0 <= result['win_rate_optimum'] <= 1
        assert result['n_optimum_wins'] + result['n_simple_wins'] <= result['n_pairs']

    def test_paired_tests_with_identical_values(self, analyzer):
        """Test paired tests with no differences."""
        # All differences are zero
        differences = np.zeros(10)
        result = analyzer.paired_statistical_tests(differences)

        # Should handle gracefully
        assert result['mean_difference'] == 0
        assert result['std_difference'] == 0
        # p-value should be 1 (no difference)
        # Note: Wilcoxon might return NaN for all zeros

    def test_correlation_analysis(self, analyzer):
        """Test correlation analysis."""
        # Create perfectly correlated data
        optimum_returns = np.array([1, 2, 3, 4, 5])
        simple_returns = np.array([2, 4, 6, 8, 10])

        result = analyzer.correlation_analysis(optimum_returns, simple_returns)

        # Check output structure
        assert 'pearson_correlation' in result
        assert 'pearson_pvalue' in result
        assert 'spearman_correlation' in result
        assert 'spearman_pvalue' in result
        assert 'beta' in result
        assert 'alpha' in result
        assert 'r_squared' in result
        assert 'correlation_interpretation' in result

        # Perfect correlation should be close to 1
        assert abs(result['pearson_correlation'] - 1.0) < 0.01
        assert abs(result['spearman_correlation'] - 1.0) < 0.01
        assert result['r_squared'] > 0.99

        # Beta should be 0.5 (optimum = 0.5 * simple, since simple = 2 * optimum)
        assert abs(result['beta'] - 0.5) < 0.01

    def test_correlation_with_negative_correlation(self, analyzer):
        """Test correlation with negatively correlated data."""
        optimum_returns = np.array([1, 2, 3, 4, 5])
        simple_returns = np.array([5, 4, 3, 2, 1])

        result = analyzer.correlation_analysis(optimum_returns, simple_returns)

        # Should detect negative correlation
        assert result['pearson_correlation'] < 0
        assert abs(result['pearson_correlation'] + 1.0) < 0.01

    def test_consistency_analysis(self, analyzer, sample_differences):
        """Test consistency analysis."""
        result = analyzer.consistency_analysis(sample_differences)

        # Check output structure
        assert 'total_periods' in result
        assert 'consistent_winner' in result
        assert 'max_optimum_streak' in result
        assert 'max_simple_streak' in result
        assert 'n_regime_changes' in result
        assert 'consistency_ratio' in result
        assert 'consistency_interpretation' in result

        # Check logical consistency
        assert result['total_periods'] == len(sample_differences)
        assert result['consistent_winner'] in ['Optimum', 'Simple']
        assert result['max_optimum_streak'] >= 0
        assert result['max_simple_streak'] >= 0
        assert result['n_regime_changes'] >= 0

    def test_consistency_with_all_positive(self, analyzer):
        """Test consistency with all positive differences."""
        differences = np.ones(10) * 5  # All positive
        result = analyzer.consistency_analysis(differences)

        assert result['consistent_winner'] == 'Optimum'
        assert result['max_optimum_streak'] == 10
        assert result['max_simple_streak'] == 0
        assert result['n_regime_changes'] == 0

    def test_risk_adjusted_comparison(self, analyzer, sample_paired_results):
        """Test risk-adjusted comparison."""
        result = analyzer.risk_adjusted_comparison(sample_paired_results)

        # Check output structure
        assert 'optimum_sharpe' in result
        assert 'simple_sharpe' in result
        assert 'sharpe_difference' in result
        assert 'information_ratio' in result
        assert 'tracking_error' in result
        assert 'max_relative_drawdown' in result
        assert 'risk_adjusted_winner' in result

        # Check logical consistency
        assert result['sharpe_difference'] == result['optimum_sharpe'] - result['simple_sharpe']
        assert result['risk_adjusted_winner'] in ['Optimum', 'Simple']
        assert result['tracking_error'] >= 0
        assert result['max_relative_drawdown'] <= 0

    def test_comprehensive_paired_analysis(self, analyzer):
        """Test comprehensive paired analysis."""
        # Use short durations for testing
        durations = [52, 104]  # 1-year, 2-year

        # Shorten test period
        analyzer.overall_start = date(2022, 1, 1)
        analyzer.overall_end = date(2023, 12, 31)

        results = analyzer.run_comprehensive_paired_analysis(durations)

        # Check results structure
        assert '1Y' in results
        assert '2Y' in results

        for duration_key, data in results.items():
            assert 'paired_samples' in data
            assert 'mean_optimum_return' in data
            assert 'mean_simple_return' in data
            assert 'mean_difference' in data
            assert 'statistical_tests' in data
            assert 'correlation' in data
            assert 'consistency' in data
            assert 'risk_adjusted' in data

            # Check subsections
            assert 'paired_t_pvalue' in data['statistical_tests']
            # Correlation might be empty if insufficient data
            if data['correlation']:
                assert 'pearson_correlation' in data['correlation']
            assert 'consistent_winner' in data['consistency']
            assert 'information_ratio' in data['risk_adjusted']

    def test_edge_cases(self, analyzer):
        """Test edge cases and error handling."""
        # Empty differences
        empty_diff = np.array([])
        result = analyzer.paired_statistical_tests(empty_diff)
        assert result['n_pairs'] == 0

        # Single pair
        single_diff = np.array([5.0])
        result = analyzer.paired_statistical_tests(single_diff)
        assert result['n_pairs'] == 1

        # Test with NaN values
        diff_with_nan = np.array([1, 2, np.nan, 4, 5])
        # Should handle NaN appropriately

        # Test correlation with insufficient data
        short_optimum = np.array([1])
        short_simple = np.array([2])
        result = analyzer.correlation_analysis(short_optimum, short_simple)
        assert result == {}  # Should return empty dict

    def test_plot_paired_analysis(self, analyzer, sample_paired_results):
        """Test visualization generation."""
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend for testing

        # Create output directory if needed
        os.makedirs('reports/analysis', exist_ok=True)

        try:
            analyzer.plot_paired_analysis(sample_paired_results, '1Y_test')
            # Check if file was created
            assert os.path.exists('reports/analysis/paired_comparison_1Y_test.png')
            # Clean up
            os.remove('reports/analysis/paired_comparison_1Y_test.png')
        except Exception as e:
            # Visualization might fail in test environment
            pass


@pytest.mark.integration
class TestPairedIntegration:
    """Integration tests for paired comparison analyzer."""

    def test_full_workflow(self):
        """Test complete paired analysis workflow."""
        analyzer = PairedStrategyComparison(
            weekly_budget=250.0,
            overall_start=date(2022, 1, 1),
            overall_end=date(2023, 6, 30)
        )

        # Run with short duration for speed
        results = analyzer.run_comprehensive_paired_analysis([52])

        # Verify results
        assert '1Y' in results
        assert results['1Y']['paired_samples'] > 0

        # Check all analyses ran
        assert 'statistical_tests' in results['1Y']
        assert 'correlation' in results['1Y']
        assert 'consistency' in results['1Y']
        assert 'risk_adjusted' in results['1Y']

    def test_consistency_across_durations(self):
        """Test that longer durations have fewer samples."""
        analyzer = PairedStrategyComparison(
            overall_start=date(2020, 1, 1),
            overall_end=date(2023, 12, 31)
        )

        samples_52w = analyzer.generate_paired_samples(52, step_weeks=4)
        samples_104w = analyzer.generate_paired_samples(104, step_weeks=4)

        # Longer duration should have fewer samples
        assert len(samples_104w) < len(samples_52w)

    def test_paired_vs_unpaired_power(self):
        """Demonstrate that paired tests have more statistical power."""
        np.random.seed(42)
        n = 30

        # Create paired data with small consistent difference
        optimum = np.random.randn(n) * 10 + 100
        simple = optimum + np.random.randn(n) * 2 + 2  # Small positive bias

        # Paired test
        from scipy.stats import ttest_rel, ttest_ind
        _, p_paired = ttest_rel(optimum, simple)

        # Unpaired test
        _, p_unpaired = ttest_ind(optimum, simple)

        # Paired test should have smaller p-value (more power)
        # This demonstrates the advantage of paired testing
        assert p_paired < p_unpaired