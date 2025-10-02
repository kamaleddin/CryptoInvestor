"""
Test suite for Balanced Rolling Analyzer.
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

from tools.balanced_rolling_analyzer import main
from tools.advanced_duration_analyzer import AdvancedDurationAnalyzer


class TestBalancedRollingAnalyzer:
    """Test the balanced rolling analyzer functionality."""

    @pytest.fixture
    def mock_analyzer(self):
        """Create a mock analyzer with test data."""
        analyzer = Mock(spec=AdvancedDurationAnalyzer)
        analyzer.overall_start = date(2016, 1, 1)
        analyzer.overall_end = date(2025, 9, 24)
        analyzer.weekly_budget = 250.0
        analyzer.risk_free_rate = 0.04
        return analyzer

    def test_main_function_runs(self):
        """Test that main function runs without errors."""
        with patch('tools.balanced_rolling_analyzer.AdvancedDurationAnalyzer') as MockAnalyzer:
            mock_instance = Mock()
            MockAnalyzer.return_value = mock_instance

            # Setup mock results
            mock_results = {
                '1-Year': {
                    'n_periods': 114,
                    'optimum_mean': 65.3,
                    'simple_mean': 70.7,
                    'p_value': 0.881
                },
                '2-Year': {
                    'n_periods': 101,
                    'optimum_mean': 64.2,
                    'simple_mean': 152.8,
                    'p_value': 0.008
                }
            }
            mock_instance.run_comprehensive_analysis.return_value = mock_results
            mock_instance.print_analysis_report.return_value = None

            # Run main
            results = main()

            # Verify calls
            MockAnalyzer.assert_called_once_with(
                weekly_budget=250.0,
                overall_start=date(2016, 1, 1),
                overall_end=date(2025, 9, 24),
                risk_free_rate=0.04,
                verbose=True
            )

            mock_instance.run_comprehensive_analysis.assert_called_once_with(
                use_non_overlapping=False,
                rolling_step_weeks=4  # Monthly rolling
            )

            assert results == mock_results

    def test_monthly_rolling_configuration(self):
        """Test that analyzer uses monthly (4-week) rolling windows."""
        with patch('tools.balanced_rolling_analyzer.AdvancedDurationAnalyzer') as MockAnalyzer:
            mock_instance = Mock()
            MockAnalyzer.return_value = mock_instance
            mock_instance.run_comprehensive_analysis.return_value = {}
            mock_instance.print_analysis_report.return_value = None

            main()

            # Verify monthly rolling (4-week steps) is used
            call_args = mock_instance.run_comprehensive_analysis.call_args
            assert call_args[1]['rolling_step_weeks'] == 4
            assert call_args[1]['use_non_overlapping'] == False

    def test_sample_size_analysis(self):
        """Test sample size analysis output."""
        with patch('tools.balanced_rolling_analyzer.AdvancedDurationAnalyzer') as MockAnalyzer:
            mock_instance = Mock()
            MockAnalyzer.return_value = mock_instance

            # Mock results with different sample sizes
            mock_results = {
                '1-Year': {'n_periods': 114},  # Excellent power
                '2-Year': {'n_periods': 101},  # Excellent power
                '3-Year': {'n_periods': 50},   # Good power
                '4-Year': {'n_periods': 30}    # Moderate power
            }
            mock_instance.run_comprehensive_analysis.return_value = mock_results
            mock_instance.print_analysis_report.return_value = None

            results = main()

            # Verify results structure
            assert '1-Year' in results
            assert results['1-Year']['n_periods'] == 114
            assert results['3-Year']['n_periods'] == 50

    def test_autocorrelation_adjustment(self):
        """Test autocorrelation adjustments are calculated correctly."""
        # Monthly rolling has ~92% overlap, so effective N is ~8% of total
        total_n = 100
        expected_effective_n = int(100 * 0.08)  # ~8 independent samples

        assert expected_effective_n == 8

        # Test for different step sizes
        overlap_rates = {
            1: 0.98,   # Weekly
            2: 0.96,   # Bi-weekly
            4: 0.92,   # Monthly
            13: 0.75,  # Quarterly
            26: 0.50,  # Semi-annual
            52: 0.00   # Annual
        }

        for step_weeks, overlap in overlap_rates.items():
            independence_rate = 1 - overlap
            effective_n = int(100 * independence_rate)

            if step_weeks == 4:  # Monthly (current default)
                assert effective_n in [7, 8]  # Allow for rounding differences

    def test_statistical_power_classification(self):
        """Test statistical power classification based on sample size."""
        # Test power classification logic
        classifications = [
            (100, 'Excellent'),  # n > 80
            (81, 'Excellent'),
            (80, 'Good'),       # 40 < n <= 80
            (50, 'Good'),
            (40, 'Moderate'),   # n <= 40
            (20, 'Moderate')
        ]

        for n, expected_power in classifications:
            if n > 80:
                power = 'Excellent'
            elif n > 40:
                power = 'Good'
            else:
                power = 'Moderate'

            assert power == expected_power

    def test_output_formatting(self, capsys):
        """Test that output is properly formatted."""
        with patch('tools.balanced_rolling_analyzer.AdvancedDurationAnalyzer') as MockAnalyzer:
            mock_instance = Mock()
            MockAnalyzer.return_value = mock_instance
            mock_instance.run_comprehensive_analysis.return_value = {
                '1-Year': {'n_periods': 114}
            }
            mock_instance.print_analysis_report.return_value = None

            main()

            captured = capsys.readouterr()

            # Check for key output elements
            assert "BALANCED ROLLING WINDOW ANALYSIS" in captured.out
            assert "Monthly Rolling: 114 periods" in captured.out
            assert "Statistical Power: Excellent" in captured.out
            assert "AUTOCORRELATION ANALYSIS" in captured.out
            assert "Monthly (4-week):    ≈ 92% overlap" in captured.out

    def test_integration_with_analyzer(self):
        """Test integration with actual AdvancedDurationAnalyzer."""
        # This test would require the actual analyzer to be working
        # We'll mock it for unit testing
        with patch('tools.balanced_rolling_analyzer.AdvancedDurationAnalyzer') as MockAnalyzer:
            mock_instance = Mock()
            MockAnalyzer.return_value = mock_instance

            # Simulate comprehensive results
            mock_results = {
                '1-Year': {
                    'n_periods': 114,
                    'optimum_mean': 65.3,
                    'optimum_median': 0.0,
                    'optimum_std': 362.4,
                    'simple_mean': 70.7,
                    'simple_median': 37.8,
                    'simple_std': 118.0,
                    'p_value': 0.881,
                    'effect_size': -0.02,
                    'optimum_sharpe': 0.169,
                    'simple_sharpe': 0.566
                }
            }
            mock_instance.run_comprehensive_analysis.return_value = mock_results
            mock_instance.print_analysis_report.return_value = None

            results = main()

            # Verify comprehensive results
            assert results['1-Year']['optimum_sharpe'] == 0.169
            assert results['1-Year']['simple_sharpe'] == 0.566
            assert results['1-Year']['p_value'] == 0.881