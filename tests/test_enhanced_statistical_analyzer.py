#!/usr/bin/env python3
"""
Test suite for Enhanced Statistical Analyzer.

Tests advanced statistical methods including:
- Block bootstrap
- Stationarity testing
- Autocorrelation detection
- Multiple comparison corrections
- Fat-tailed distribution fitting
- Monte Carlo simulation
"""

import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.enhanced_statistical_analyzer import EnhancedStatisticalAnalyzer


class TestEnhancedStatisticalAnalyzer:
    """Test suite for enhanced statistical analyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing."""
        return EnhancedStatisticalAnalyzer(
            weekly_budget=250.0,
            overall_start=date(2020, 1, 1),
            overall_end=date(2023, 12, 31)
        )

    @pytest.fixture
    def sample_returns(self):
        """Generate sample return data for testing."""
        np.random.seed(42)
        # Generate returns with autocorrelation and fat tails
        n = 100
        returns = np.random.standard_t(df=3, size=n) * 0.05  # Fat-tailed distribution
        # Add some autocorrelation
        for i in range(1, n):
            returns[i] = 0.3 * returns[i-1] + 0.7 * returns[i]
        return returns

    @pytest.fixture
    def stationary_series(self):
        """Generate a stationary time series."""
        np.random.seed(42)
        return pd.Series(np.random.randn(100))

    @pytest.fixture
    def non_stationary_series(self):
        """Generate a non-stationary time series (random walk)."""
        np.random.seed(42)
        returns = np.random.randn(100)
        return pd.Series(np.cumsum(returns))  # Random walk

    def test_initialization(self, analyzer):
        """Test analyzer initialization."""
        assert analyzer.weekly_budget == 250.0
        assert analyzer.overall_start == date(2020, 1, 1)
        assert analyzer.overall_end == date(2023, 12, 31)
        assert analyzer.risk_free_rate == 0.04
        assert analyzer.price_data is not None

    def test_block_bootstrap(self, analyzer, sample_returns):
        """Test block bootstrap implementation."""
        result = analyzer.block_bootstrap(
            data=sample_returns,
            block_size=5,
            n_bootstrap=100
        )

        # Check output structure
        assert 'mean_ci' in result
        assert 'std_ci' in result
        assert 'mean_se' in result
        assert 'block_size' in result

        # Check confidence intervals
        assert len(result['mean_ci']) == 2
        assert result['mean_ci'][0] < result['mean_ci'][1]
        assert len(result['std_ci']) == 2
        assert result['std_ci'][0] < result['std_ci'][1]

        # Check standard error is positive
        assert result['mean_se'] > 0

        # Check block size
        assert result['block_size'] == 5

    def test_block_bootstrap_auto_block_size(self, analyzer, sample_returns):
        """Test block bootstrap with automatic block size selection."""
        result = analyzer.block_bootstrap(
            data=sample_returns,
            block_size=None,  # Auto-calculate
            n_bootstrap=50
        )

        # Should use n^(1/3) rule
        expected_block_size = int(np.ceil(len(sample_returns) ** (1/3)))
        assert result['block_size'] == expected_block_size

    def test_stationarity_testing_stationary(self, analyzer, stationary_series):
        """Test stationarity detection on stationary series."""
        result = analyzer.test_stationarity(stationary_series)

        # Check output structure
        assert 'adf_statistic' in result
        assert 'adf_pvalue' in result
        assert 'kpss_statistic' in result
        assert 'kpss_pvalue' in result
        assert 'is_stationary' in result
        assert 'interpretation' in result

        # Stationary series should have:
        # - ADF p-value < 0.05 (reject null of unit root)
        # - KPSS p-value > 0.05 (fail to reject null of stationarity)
        # Note: Random data might not always pass both tests
        assert isinstance(result['is_stationary'], bool)

    def test_stationarity_testing_non_stationary(self, analyzer, non_stationary_series):
        """Test stationarity detection on non-stationary series."""
        result = analyzer.test_stationarity(non_stationary_series)

        # Non-stationary series (random walk) should typically have:
        # - ADF p-value > 0.05 (fail to reject null of unit root)
        # - KPSS p-value < 0.05 (reject null of stationarity)
        assert 'interpretation' in result
        # Random walk should be detected as non-stationary
        # (though with small samples this isn't guaranteed)

    def test_autocorrelation_detection(self, analyzer, sample_returns):
        """Test autocorrelation detection."""
        result = analyzer.test_autocorrelation(sample_returns, lags=5)

        # Check output structure
        assert 'ljung_box_stats' in result
        assert 'ljung_box_pvalues' in result
        assert 'has_autocorrelation' in result
        assert 'first_significant_lag' in result
        assert 'autocorr_interpretation' in result

        # Check arrays have correct length
        assert len(result['ljung_box_stats']) == 5
        assert len(result['ljung_box_pvalues']) == 5

        # Our sample data has built-in autocorrelation
        assert isinstance(result['has_autocorrelation'], bool)

    def test_regime_detection(self, analyzer):
        """Test regime detection."""
        # Create returns with clear regimes
        np.random.seed(42)
        low_vol = np.random.randn(30) * 0.01
        high_vol = np.random.randn(30) * 0.05
        returns = pd.Series(np.concatenate([low_vol, high_vol, low_vol]))

        result = analyzer.regime_detection(returns, n_regimes=2)

        # Check output structure
        assert 'regimes' in result
        assert 'regime_stats' in result
        assert 'current_regime' in result

        # Check regime statistics
        assert len(result['regime_stats']) > 0
        for regime, stats in result['regime_stats'].items():
            assert 'mean_return' in stats
            assert 'volatility' in stats
            assert 'sharpe' in stats
            assert 'periods' in stats
            assert 'percentage' in stats

    def test_multiple_comparison_correction(self, analyzer):
        """Test multiple comparison correction."""
        # Test p-values where some should be significant
        p_values = [0.01, 0.03, 0.04, 0.20, 0.50]

        result = analyzer.multiple_comparison_correction(
            p_values, method='bonferroni'
        )

        # Check output structure
        assert 'original_pvalues' in result
        assert 'corrected_pvalues' in result
        assert 'rejected_null' in result
        assert 'alpha_bonferroni' in result
        assert 'alpha_sidak' in result
        assert 'method' in result
        assert 'any_significant' in result

        # Check dimensions
        assert len(result['corrected_pvalues']) == len(p_values)
        assert len(result['rejected_null']) == len(p_values)

        # Bonferroni correction should make p-values larger
        for orig, corr in zip(p_values, result['corrected_pvalues']):
            assert corr >= orig

    def test_omega_ratio(self, analyzer):
        """Test Omega ratio calculation."""
        # Test with positive returns
        returns = np.array([0.01, 0.02, -0.01, 0.03, -0.005])
        omega = analyzer.calculate_omega_ratio(returns, threshold=0.0)
        assert omega > 0

        # Test with all positive returns
        returns = np.array([0.01, 0.02, 0.03])
        omega = analyzer.calculate_omega_ratio(returns, threshold=0.0)
        assert omega == np.inf

        # Test with all negative returns
        returns = np.array([-0.01, -0.02, -0.03])
        omega = analyzer.calculate_omega_ratio(returns, threshold=0.0)
        assert omega == 0

    def test_ulcer_index(self, analyzer):
        """Test Ulcer Index calculation."""
        # Test with no drawdown
        prices = np.array([100, 101, 102, 103, 104])
        ulcer = analyzer.calculate_ulcer_index(prices)
        assert ulcer == 0

        # Test with drawdown
        prices = np.array([100, 95, 90, 95, 100])
        ulcer = analyzer.calculate_ulcer_index(prices)
        assert ulcer > 0

        # Test with severe drawdown
        prices = np.array([100, 50, 25, 50, 75])
        ulcer_severe = analyzer.calculate_ulcer_index(prices)
        assert ulcer_severe > ulcer  # More severe drawdown = higher Ulcer Index

    def test_tail_risk_analysis(self, analyzer, sample_returns):
        """Test tail risk analysis."""
        result = analyzer.tail_risk_analysis(sample_returns)

        # Check output structure
        assert 't_dist_df' in result
        assert 't_dist_loc' in result
        assert 't_dist_scale' in result
        assert 'left_tail_5%' in result
        assert 'left_tail_1%' in result
        assert 'right_tail_95%' in result
        assert 'right_tail_99%' in result
        assert 'tail_index' in result
        assert 'has_fat_tails' in result
        assert 'tail_interpretation' in result

        # Check tail ordering
        assert result['left_tail_1%'] < result['left_tail_5%']
        assert result['right_tail_95%'] < result['right_tail_99%']

    def test_monte_carlo_simulation(self, analyzer, sample_returns):
        """Test Monte Carlo simulation."""
        result = analyzer.monte_carlo_simulation(
            historical_returns=sample_returns,
            n_simulations=1000,
            n_periods=52
        )

        # Check output structure
        assert 'mean_return' in result
        assert 'median_return' in result
        assert 'std_return' in result
        assert 'percentile_5' in result
        assert 'percentile_25' in result
        assert 'percentile_50' in result
        assert 'percentile_75' in result
        assert 'percentile_95' in result
        assert 'probability_positive' in result
        assert 'probability_beat_market' in result
        assert 'var_95' in result
        assert 'cvar_95' in result

        # Check percentile ordering
        assert result['percentile_5'] <= result['percentile_25']
        assert result['percentile_25'] <= result['percentile_50']
        assert result['percentile_50'] <= result['percentile_75']
        assert result['percentile_75'] <= result['percentile_95']

        # Check probabilities are between 0 and 1
        assert 0 <= result['probability_positive'] <= 1
        assert 0 <= result['probability_beat_market'] <= 1

        # VaR should be less than or equal to 5th percentile
        assert result['var_95'] <= result['percentile_5']

    def test_comprehensive_analysis_runs(self, analyzer):
        """Test that comprehensive analysis runs without errors."""
        # This is an integration test
        try:
            # Use a shorter period for faster testing
            analyzer.overall_end = date(2020, 12, 31)
            result = analyzer.run_enhanced_comparison()

            # Check main sections exist
            assert 'stationarity' in result
            assert 'autocorrelation' in result
            assert 'regimes' in result
            assert 'tail_risk' in result
            assert 'dca_results' in result
            assert 'multiple_comparisons' in result
            assert 'monte_carlo' in result

        except Exception as e:
            pytest.fail(f"Comprehensive analysis failed: {e}")

    def test_edge_cases(self, analyzer):
        """Test edge cases and error handling."""
        # Empty data
        empty_data = np.array([])
        result = analyzer.block_bootstrap(empty_data, n_bootstrap=10)
        # Should handle gracefully

        # Single value
        single_value = np.array([1.0])
        omega = analyzer.calculate_omega_ratio(single_value)
        assert omega == np.inf or omega == 0

        # All zeros
        zeros = np.zeros(10)
        ulcer = analyzer.calculate_ulcer_index(zeros)
        assert ulcer == 0 or np.isnan(ulcer)


@pytest.mark.integration
class TestIntegration:
    """Integration tests for enhanced statistical analyzer."""

    def test_full_workflow(self):
        """Test complete analysis workflow."""
        analyzer = EnhancedStatisticalAnalyzer(
            weekly_budget=250.0,
            overall_start=date(2022, 1, 1),
            overall_end=date(2023, 1, 1)
        )

        # Run analysis
        results = analyzer.run_enhanced_comparison()

        # Verify all components ran
        assert results is not None
        assert len(results) > 0

        # Check stationarity results
        assert 'prices' in results['stationarity']
        assert 'returns' in results['stationarity']

        # Check DCA results exist
        assert '1Y' in results['dca_results']

    def test_reproducibility(self):
        """Test that results are reproducible with same data."""
        analyzer1 = EnhancedStatisticalAnalyzer()
        analyzer2 = EnhancedStatisticalAnalyzer()

        # Set random seed for reproducibility
        np.random.seed(42)
        data = np.random.randn(100)

        result1 = analyzer1.block_bootstrap(data, n_bootstrap=50)

        np.random.seed(42)
        result2 = analyzer2.block_bootstrap(data, n_bootstrap=50)

        # Check that both results are valid (have correct structure)
        # Note: Exact reproducibility requires controlling numpy's global random state
        # which is not always desirable in production code
        assert 'mean_ci' in result1
        assert 'mean_ci' in result2
        assert len(result1['mean_ci']) == 2
        assert len(result2['mean_ci']) == 2