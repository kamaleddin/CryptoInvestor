"""
Test suite for Advanced Duration Analyzer.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../tools'))

from tools.advanced_duration_analyzer import AdvancedDurationAnalyzer


class TestAdvancedDurationAnalyzer:
    """Test the advanced duration analyzer functionality."""

    @pytest.fixture
    def analyzer(self):
        """Create an analyzer instance for testing."""
        with patch('tools.advanced_duration_analyzer.FlexibleOptimumDCA'):
            analyzer = AdvancedDurationAnalyzer(
                weekly_budget=250.0,
                overall_start=date(2016, 1, 1),
                overall_end=date(2025, 9, 24),
                risk_free_rate=0.04,
                verbose=False
            )
            return analyzer

    @pytest.fixture
    def mock_dca(self):
        """Create a mock DCA analyzer."""
        mock = Mock()
        mock.run_optimum_dca_simulation.return_value = {
            'profit_pct': 100.0,
            'total_value': 10000.0,
            'total_btc': 0.5,
            'total_investment': 5000.0
        }
        mock.run_simple_dca_simulation.return_value = {
            'profit_pct': 80.0,
            'total_value': 9000.0,
            'total_btc': 0.45,
            'total_investment': 5000.0
        }
        return mock

    def test_initialization(self):
        """Test AdvancedDurationAnalyzer initialization."""
        analyzer = AdvancedDurationAnalyzer(
            weekly_budget=500.0,
            overall_start=date(2020, 1, 1),
            overall_end=date(2024, 12, 31),
            risk_free_rate=0.05,
            verbose=True
        )

        assert analyzer.weekly_budget == 500.0
        assert analyzer.overall_start == date(2020, 1, 1)
        assert analyzer.overall_end == date(2024, 12, 31)
        assert analyzer.risk_free_rate == 0.05
        assert analyzer.verbose == True

    def test_calculate_sharpe_ratio(self, analyzer):
        """Test Sharpe ratio calculation."""
        returns = [0.1, 0.2, -0.05, 0.15, 0.08]

        sharpe = analyzer.calculate_sharpe_ratio(returns)

        # Calculate expected Sharpe (implementation uses annualized Sharpe)
        returns_array = np.array(returns)
        mean_return = np.mean(returns_array)
        std_return = np.std(returns_array, ddof=1)

        # The implementation annualizes the Sharpe ratio
        sharpe_ratio = (mean_return - 0.04/52) / std_return
        expected_sharpe = sharpe_ratio * np.sqrt(52)  # Annualized

        assert abs(sharpe - expected_sharpe) < 0.001

    def test_calculate_sortino_ratio(self, analyzer):
        """Test Sortino ratio calculation."""
        returns = np.array([0.1, 0.2, -0.05, 0.15, -0.02])  # Convert to numpy array

        sortino = analyzer.calculate_sortino_ratio(returns)

        # Calculate expected Sortino (implementation uses annualized)
        mean_return = np.mean(returns)
        # Only negative excess returns for downside deviation
        downside_returns = returns[returns < 0]

        if len(downside_returns) > 0:
            downside_std = np.std(downside_returns, ddof=1)
            if downside_std > 0:
                # Annualized Sortino like the implementation
                sortino_ratio = (mean_return - 0.04/52) / downside_std
                expected_sortino = sortino_ratio * np.sqrt(52)
            else:
                expected_sortino = float('inf')
        else:
            expected_sortino = float('inf')

        if sortino == float('inf') and expected_sortino == float('inf'):
            assert True
        else:
            assert abs(sortino - expected_sortino) < 0.001

    def test_calculate_max_drawdown(self, analyzer):
        """Test maximum drawdown calculation."""
        returns = [0.1, 0.2, -0.3, 0.15, 0.1]

        # Calculate cumulative returns first
        cumulative = []
        cum_return = 1.0
        for r in returns:
            cum_return *= (1 + r)
            cumulative.append(cum_return)

        # The method expects cumulative returns and returns a dict
        max_dd_dict = analyzer.calculate_max_drawdown(np.array(cumulative))

        # Extract the max drawdown value from the dict
        max_dd = max_dd_dict['max_drawdown']

        # Calculate expected drawdown (implementation returns negative)
        peak = cumulative[0]
        max_drawdown = 0
        for value in cumulative:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        # The implementation returns negative drawdown
        expected_drawdown = -max_drawdown if max_drawdown > 0 else 0

        assert abs(max_dd - expected_drawdown) < 0.001

    def test_calculate_calmar_ratio(self, analyzer):
        """Test Calmar ratio calculation."""
        total_return = 0.5  # 50% total return
        max_drawdown = -0.2  # 20% drawdown
        years = 2.0

        calmar = analyzer.calculate_calmar_ratio(total_return, max_drawdown, years)

        # Calculate expected Calmar
        annualized_return = (1 + total_return) ** (1 / years) - 1
        expected_calmar = annualized_return / abs(max_drawdown)

        assert abs(calmar - expected_calmar) < 0.001

    def test_calculate_var(self, analyzer):
        """Test Value at Risk calculation."""
        returns = np.random.normal(0.1, 0.2, 100)  # Normal returns

        # The method is actually calculate_var_cvar and returns both
        result = analyzer.calculate_var_cvar(returns, confidence=0.95)
        var_95 = result['var']

        # VaR is the 5th percentile (implementation returns positive value)
        expected_var = np.percentile(returns, 5)

        assert abs(var_95 - expected_var) < 0.01

    def test_calculate_cvar(self, analyzer):
        """Test Conditional Value at Risk calculation."""
        returns = np.random.normal(0.1, 0.2, 100)

        # The method is actually calculate_var_cvar and returns both
        result = analyzer.calculate_var_cvar(returns, confidence=0.95)
        cvar_95 = result['cvar']

        # CVaR is the average of returns below VaR (implementation returns positive)
        var_threshold = np.percentile(returns, 5)
        tail_returns = [r for r in returns if r <= var_threshold]
        expected_cvar = np.mean(tail_returns) if tail_returns else 0

        assert abs(cvar_95 - expected_cvar) < 0.01

    # Removed test_run_period_simulation as the method doesn't exist

    def test_bootstrap_confidence_interval(self, analyzer):
        """Test bootstrap confidence interval calculation."""
        data = np.random.normal(10, 5, 100)

        # bootstrap_confidence_interval returns (point_estimate, lower, upper)
        point_estimate, ci_lower, ci_upper = analyzer.bootstrap_confidence_interval(
            data,
            statistic_func=np.mean,
            n_bootstrap=100
        )

        # Check CI structure
        assert ci_lower < ci_upper  # Lower bound should be less than upper
        assert abs(point_estimate - np.mean(data)) < 0.001  # Point estimate should be the mean

        # Mean should be within CI
        mean_val = np.mean(data)
        assert ci_lower <= mean_val <= ci_upper

    def test_statistical_significance_test(self, analyzer):
        """Test statistical significance testing functionality."""
        # Test with significant difference
        optimum = np.random.normal(100, 10, 50)
        simple = np.random.normal(80, 10, 50)

        result = analyzer.statistical_significance_test(optimum, simple)

        # Check result keys based on actual implementation
        assert 't_pvalue' in result
        assert 'u_pvalue' in result  # Changed from mw_pvalue to u_pvalue
        assert 'cohens_d' in result
        assert 'significant_at_5pct' in result
        assert 'significant_at_1pct' in result

        assert 0 <= result['t_pvalue'] <= 1
        assert result['cohens_d'] > 0  # Optimum has higher mean

        # Test with no difference - use same array, not two random arrays
        same_returns = np.random.normal(100, 10, 50)
        result2 = analyzer.statistical_significance_test(same_returns, same_returns)

        # When comparing identical arrays, t_pvalue might be NaN or very close to 0
        assert result2['cohens_d'] == 0.0 or abs(result2['cohens_d']) < 0.0001

    def test_run_comprehensive_analysis(self, analyzer, mock_dca):
        """Test comprehensive analysis across multiple durations."""
        with patch('tools.advanced_duration_analyzer.FlexibleOptimumDCA', return_value=mock_dca):
            results = analyzer.run_comprehensive_analysis(
                use_non_overlapping=False,
                rolling_step_weeks=13
            )

            # Check results for at least one duration
            assert len(results) > 0

            # Verify structure for any duration that exists
            for duration_key in results.keys():
                assert 'n_periods' in results[duration_key]
                assert 'optimum' in results[duration_key]
                assert 'simple' in results[duration_key]
                assert 'comparison' in results[duration_key]

                # Check nested structure
                assert 'mean_return' in results[duration_key]['optimum']
                assert 'mean_return' in results[duration_key]['simple']
                assert 'significance' in results[duration_key]['comparison']

    def test_print_analysis_report(self, analyzer, capsys):
        """Test printing analysis report."""
        results = {
            '1-Year': {
                'n_periods': 100,
                'years': 1.0,
                'optimum': {
                    'mean_return': 0.653,
                    'median_return': 0.40,
                    'std_return': 0.50,
                    'sharpe_ratio': 0.169,
                    'sortino_ratio': 0.25,
                    'max_drawdown': 0.3,
                    'var_95': 0.1,
                    'cvar_95': 0.15,
                    'win_rate': 0.45,
                    'mean_ci': (0.6, 0.65, 0.7),
                    'distribution': {'skewness': 0.5, 'kurtosis': 3.0, 'is_normal': False}
                },
                'simple': {
                    'mean_return': 0.707,
                    'median_return': 0.55,
                    'std_return': 0.30,
                    'sharpe_ratio': 0.566,
                    'sortino_ratio': 0.8,
                    'max_drawdown': 0.2,
                    'var_95': 0.08,
                    'cvar_95': 0.12,
                    'win_rate': 0.55,
                    'mean_ci': (0.68, 0.71, 0.74),
                    'distribution': {'skewness': 0.3, 'kurtosis': 2.8, 'is_normal': False}
                },
                'comparison': {
                    'mean_outperformance': -0.054,
                    'median_outperformance': -0.15,
                    'outperformance_rate': 0.45,
                    'significance': {
                        't_statistic': -0.15,  # Added missing t_statistic
                        't_pvalue': 0.881,
                        'u_pvalue': 0.9,
                        'cohens_d': -0.02,
                        'significant_at_5pct': False,
                        'significant_at_1pct': False
                    }
                }
            }
        }

        analyzer.print_analysis_report(results)

        captured = capsys.readouterr()

        # Check key elements in output
        assert "1-YEAR DURATION" in captured.out
        assert "Sample Size: 100" in captured.out
        assert "Mean Return:" in captured.out
        assert "65.30%" in captured.out or "65.3%" in captured.out  # optimum mean
        assert "70.70%" in captured.out or "70.7%" in captured.out  # simple mean
        assert "Sharpe Ratio:" in captured.out

    def test_edge_cases(self, analyzer):
        """Test edge cases and error handling."""
        # Test with empty returns
        sharpe = analyzer.calculate_sharpe_ratio(np.array([]))
        assert sharpe == 0

        # Test with single return
        sortino = analyzer.calculate_sortino_ratio(np.array([0.1]))
        assert sortino == float('inf') or sortino == 0

        # Test with all positive returns (no drawdown)
        cumulative = np.array([1.1, 1.3, 1.6])  # Cumulative returns, not individual
        max_dd_dict = analyzer.calculate_max_drawdown(cumulative)
        assert max_dd_dict['max_drawdown'] == 0

        # Test VaR with few samples
        var_result = analyzer.calculate_var_cvar(np.array([0.1, 0.2]), confidence=0.95)
        assert isinstance(var_result['var'], (int, float))

    def test_verbose_output(self, analyzer, capsys):
        """Test verbose output during analysis."""
        analyzer.verbose = True

        # Limit duration for faster test
        analyzer.durations = {'1-Year': 52}  # Only test 1 year
        analyzer.overall_start = date(2024, 1, 1)
        analyzer.overall_end = date(2025, 1, 1)

        with patch('tools.advanced_duration_analyzer.FlexibleOptimumDCA') as MockDCA:
            mock_instance = Mock()
            MockDCA.return_value = mock_instance
            mock_instance.run_optimum_dca_simulation.return_value = {
                'profit_pct': 100.0,
                'holding_value': 10000.0,
                'total_btc': 0.5,
                'total_investment': 5000.0
            }
            mock_instance.run_simple_dca_simulation.return_value = {
                'profit_pct': 80.0,
                'holding_value': 9000.0,
                'total_btc': 0.45,
                'total_investment': 5000.0
            }

            analyzer.run_comprehensive_analysis(use_non_overlapping=True)

            captured = capsys.readouterr()
            # Should have progress output when verbose=True
            assert "ADVANCED STATISTICAL ANALYSIS" in captured.out
            assert len(captured.out) > 0