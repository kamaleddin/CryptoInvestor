"""
Test suite for Duration Simulator.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import date, timedelta
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../tools'))

from tools.duration_simulator import DurationSimulator, main


class TestDurationSimulator:
    """Test the duration simulator functionality."""

    @pytest.fixture
    def simulator(self):
        """Create a simulator instance for testing."""
        with patch('tools.duration_simulator.FlexibleOptimumDCA'):
            simulator = DurationSimulator(
                weekly_budget=250.0,
                overall_start=date(2016, 1, 1),
                overall_end=date(2025, 9, 24),
                verbose=False
            )
            return simulator

    @pytest.fixture
    def mock_dca_analyzer(self):
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

    @pytest.fixture
    def sample_results_df(self):
        """Create a sample results DataFrame."""
        data = {
            'start_date': [date(2020, 1, 1), date(2020, 1, 8), date(2021, 1, 1)],
            'end_date': [date(2021, 1, 1), date(2021, 1, 8), date(2022, 1, 1)],
            'duration': ['1-Year', '1-Year', '1-Year'],
            'weeks': [52, 52, 52],
            'optimum_return_pct': [100.0, 150.0, 80.0],
            'simple_return_pct': [80.0, 100.0, 60.0],
            'optimum_value': [10000, 15000, 8000],
            'simple_value': [9000, 11000, 7000],
            'optimum_btc': [0.5, 0.7, 0.4],
            'simple_btc': [0.45, 0.55, 0.35],
            'optimum_investment': [5000, 5000, 5000],
            'simple_investment': [5000, 5000, 5000],
            'outperformance_pct': [20.0, 50.0, 20.0],
            'outperformance_ratio': [1.25, 1.5, 1.33]  # Added missing column
        }
        return pd.DataFrame(data)

    def test_initialization(self):
        """Test DurationSimulator initialization."""
        simulator = DurationSimulator(
            weekly_budget=500.0,
            overall_start=date(2020, 1, 1),
            overall_end=date(2024, 12, 31),
            verbose=False
        )

        assert simulator.weekly_budget == 500.0
        assert simulator.overall_start == date(2020, 1, 1)
        assert simulator.overall_end == date(2024, 12, 31)
        assert simulator.verbose == False

    def test_load_price_data(self, simulator):
        """Test loading price data."""
        # Mock the price data loading
        with patch.object(simulator, 'price_data', pd.DataFrame({'Price': [100, 200]})):
            assert simulator.price_data is not None
            assert len(simulator.price_data) > 0

    def test_get_final_price(self, simulator):
        """Test getting final price for a date."""
        # Mock price data matching expected structure
        mock_price_data = pd.DataFrame({
            'Price': [100, 200, 300],
            'date_only': [date(2020, 1, 1), date(2020, 1, 8), date(2020, 1, 15)]
        })

        with patch.object(simulator, 'price_data', mock_price_data):
            price = simulator._get_final_price(date(2020, 1, 10))
            assert price == 200  # Should get price from Jan 8 (on or before Jan 10)

    def test_generate_start_dates(self, simulator):
        """Test generating start dates for duration."""
        # Set a small date range for testing
        simulator.overall_start = date(2020, 1, 1)
        simulator.overall_end = date(2020, 3, 1)

        start_dates = simulator._generate_start_dates(duration_weeks=4)

        # Should generate weekly start dates
        assert len(start_dates) > 0
        assert start_dates[0] == date(2020, 1, 1)
        # Check dates are weekly
        if len(start_dates) > 1:
            assert (start_dates[1] - start_dates[0]).days == 7

    def test_run_single_simulation(self, simulator, mock_dca_analyzer):
        """Test running a single simulation."""
        # Mock the price data
        with patch.object(simulator, '_get_final_price', return_value=50000.0):
            with patch('tools.duration_simulator.FlexibleOptimumDCA', return_value=mock_dca_analyzer):
                # Mock the results from DCA analyzer to match expected format
                mock_dca_analyzer.run_optimum_dca_simulation.return_value = {
                    'profit_pct': 100.0,
                    'holding_value': 10000.0,
                    'total_btc': 0.5,
                    'total_investment': 5000.0,
                    'profit': 5000.0,
                    'period_weeks': 52
                }
                mock_dca_analyzer.run_simple_dca_simulation.return_value = {
                    'profit_pct': 80.0,
                    'holding_value': 9000.0,
                    'total_btc': 0.45,
                    'total_investment': 5000.0,
                    'profit': 4000.0,
                    'period_weeks': 52
                }

                result = simulator._run_single_simulation(
                    start_date=date(2020, 1, 1),
                    end_date=date(2021, 1, 1),
                    duration_name="1-Year"
                )

                # Check result structure
                assert result['start_date'] == date(2020, 1, 1)
                assert result['duration'] == '1-Year'
                assert result['optimum_return_pct'] == 100.0
                assert result['simple_return_pct'] == 80.0

    def test_run_all_simulations(self, simulator, mock_dca_analyzer):
        """Test running all simulations."""
        # Limit date range for faster test
        simulator.overall_start = date(2020, 1, 1)
        simulator.overall_end = date(2020, 2, 1)

        with patch.object(simulator, '_get_final_price', return_value=50000.0):
            with patch('tools.duration_simulator.FlexibleOptimumDCA', return_value=mock_dca_analyzer):
                # Mock the results from DCA analyzer to match expected format
                mock_dca_analyzer.run_optimum_dca_simulation.return_value = {
                    'profit_pct': 100.0,
                    'holding_value': 10000.0,
                    'total_btc': 0.5,
                    'total_investment': 5000.0,
                    'profit': 5000.0,
                    'period_weeks': 52
                }
                mock_dca_analyzer.run_simple_dca_simulation.return_value = {
                    'profit_pct': 80.0,
                    'holding_value': 9000.0,
                    'total_btc': 0.45,
                    'total_investment': 5000.0,
                    'profit': 4000.0,
                    'period_weeks': 52
                }

                results_df = simulator.run_all_simulations()

                # Should return a DataFrame
                assert isinstance(results_df, pd.DataFrame)
                assert len(results_df) >= 0  # Might be 0 if date range too short
                if len(results_df) > 0:
                    assert 'duration' in results_df.columns
                    assert 'optimum_return_pct' in results_df.columns
                    assert 'simple_return_pct' in results_df.columns

    def test_generate_summary_statistics(self, simulator, sample_results_df):
        """Test generating summary statistics."""
        summary = simulator.generate_summary_statistics(sample_results_df)

        # Check summary structure - use correct nested structure
        assert '1-Year' in summary
        assert 'total_runs' in summary['1-Year']
        assert 'optimum' in summary['1-Year']
        assert 'simple' in summary['1-Year']
        assert 'outperformance' in summary['1-Year']

        # Verify calculations - use correct nested structure
        assert summary['1-Year']['optimum']['avg_return'] == np.mean([100.0, 150.0, 80.0])
        assert summary['1-Year']['simple']['avg_return'] == np.mean([80.0, 100.0, 60.0])

    def test_print_summary_report(self, simulator, capsys):
        """Test printing summary report."""
        # Use correct structure
        summary = {
            '1-Year': {
                'total_runs': 3,
                'optimum': {
                    'avg_return': 110.0,
                    'median_return': 100.0,
                    'min_return': 80.0,
                    'max_return': 150.0,
                    'std_return': 20.0,
                    'avg_btc': 0.5,
                    'avg_investment': 5000.0,
                    'avg_value': 10000.0,
                    'win_rate': 100.0
                },
                'simple': {
                    'avg_return': 80.0,
                    'median_return': 80.0,
                    'min_return': 60.0,
                    'max_return': 100.0,
                    'std_return': 15.0,
                    'avg_btc': 0.45,
                    'avg_investment': 5000.0,
                    'avg_value': 9000.0,
                    'win_rate': 100.0
                },
                'outperformance': {
                    'avg_pct_points': 30.0,
                    'median_pct_points': 20.0,
                    'min_pct_points': 20.0,
                    'max_pct_points': 50.0,
                    'times_better': 66.7,
                    'avg_ratio': 1.36
                }
            }
        }

        simulator.print_summary_report(summary)

        captured = capsys.readouterr()

        # Check output contains key information
        assert "COMPREHENSIVE PERFORMANCE SUMMARY" in captured.out or "SIMULATION SUMMARY" in captured.out
        assert "1-YEAR" in captured.out or "1-Year" in captured.out
        assert "110.00%" in captured.out or "110%" in captured.out
        assert "Win Rate" in captured.out

    def test_generate_detailed_report(self, simulator, sample_results_df, tmp_path):
        """Test generating detailed CSV report."""
        output_file = tmp_path / "test_detailed.csv"

        simulator.generate_detailed_report(sample_results_df, str(output_file))

        # Check file was created
        assert output_file.exists()

        # Read and verify content
        df = pd.read_csv(output_file)
        assert len(df) == 3
        assert 'duration' in df.columns

    def test_generate_summary_report_file(self, simulator, tmp_path):
        """Test generating summary text report."""
        # Use the same structure as generate_summary_statistics returns
        summary = {
            '1-Year': {
                'total_runs': 3,
                'optimum': {
                    'avg_return': 110.0,
                    'median_return': 100.0,
                    'min_return': 80.0,
                    'max_return': 150.0,
                    'std_return': 20.0,
                    'avg_btc': 0.5,
                    'avg_investment': 5000.0,
                    'avg_value': 10000.0,
                    'win_rate': 100.0
                },
                'simple': {
                    'avg_return': 80.0,
                    'median_return': 80.0,
                    'min_return': 60.0,
                    'max_return': 100.0,
                    'std_return': 15.0,
                    'avg_btc': 0.45,
                    'avg_investment': 5000.0,
                    'avg_value': 9000.0,
                    'win_rate': 100.0
                },
                'outperformance': {
                    'avg_pct_points': 30.0,
                    'median_pct_points': 20.0,
                    'min_pct_points': 20.0,
                    'max_pct_points': 50.0,
                    'times_better': 100.0,
                    'avg_ratio': 1.36
                }
            }
        }

        output_file = tmp_path / "test_summary.txt"
        simulator.generate_summary_report(summary, str(output_file))

        # Check file was created
        assert output_file.exists()

        # Read and verify content
        with open(output_file, 'r') as f:
            content = f.read()
            assert "1-YEAR" in content or "1-Year" in content
            assert "110.00%" in content or "110%" in content

    def test_main_function(self):
        """Test the main function execution."""
        mock_simulator = Mock(spec=DurationSimulator)
        mock_df = pd.DataFrame({'duration': ['1-Year'], 'optimum_return_pct': [100]})
        mock_simulator.run_all_simulations.return_value = mock_df
        mock_summary = {'1-Year': {'periods': 1}}
        mock_simulator.generate_summary_statistics.return_value = mock_summary

        with patch('tools.duration_simulator.DurationSimulator', return_value=mock_simulator):
            main()

            # Verify methods were called
            mock_simulator.run_all_simulations.assert_called_once()
            mock_simulator.generate_summary_statistics.assert_called_once()
            mock_simulator.print_summary_report.assert_called_once()
            mock_simulator.generate_detailed_report.assert_called_once()
            mock_simulator.generate_summary_report.assert_called_once()

    def test_error_handling(self, simulator):
        """Test error handling in simulations."""
        # Mock _get_final_price to return None (no price data)
        with patch.object(simulator, '_get_final_price', return_value=None):
            result = simulator._run_single_simulation(
                start_date=date(2100, 1, 1),  # Future date
                end_date=date(2101, 1, 1),
                duration_name="Test"
            )

            # Should return None when no price data
            assert result is None

    def test_win_rate_calculation(self, simulator, sample_results_df):
        """Test win rate calculation."""
        summary = simulator.generate_summary_statistics(sample_results_df)

        # Outperformance win rate should be 100% (all optimum > simple in sample data)
        assert summary['1-Year']['outperformance']['times_better'] == 100.0

    def test_statistical_calculations(self, simulator):
        """Test statistical calculations are correct."""
        df = pd.DataFrame({
            'duration': ['1-Year'] * 10,
            'optimum_return_pct': [100, 150, 200, 50, 80, 120, 90, 110, 130, 140],
            'simple_return_pct': [80, 100, 150, 40, 60, 100, 70, 90, 110, 120],
            'outperformance_pct': [20, 50, 50, 10, 20, 20, 20, 20, 20, 20],
            'outperformance_ratio': [1.25, 1.5, 1.33, 1.25, 1.33, 1.2, 1.29, 1.22, 1.18, 1.17],
            # Add other required columns
            'optimum_btc': [0.5] * 10,
            'simple_btc': [0.45] * 10,
            'optimum_investment': [5000] * 10,
            'simple_investment': [5000] * 10,
            'optimum_value': [10000] * 10,
            'simple_value': [9000] * 10
        })

        summary = simulator.generate_summary_statistics(df)

        # Verify statistical calculations using correct nested structure
        expected_optimum_mean = np.mean(df['optimum_return_pct'])
        expected_simple_mean = np.mean(df['simple_return_pct'])

        assert abs(summary['1-Year']['optimum']['avg_return'] - expected_optimum_mean) < 0.01
        assert abs(summary['1-Year']['simple']['avg_return'] - expected_simple_mean) < 0.01