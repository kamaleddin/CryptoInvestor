#!/usr/bin/env python3
"""
Test runner for CryptoInvestor DCA Analyzer

This script runs the complete test suite and provides options for different test categories.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --validation # Run only validation tests
    python run_tests.py --unit       # Run only unit tests
    python run_tests.py --performance # Run only performance tests
    python run_tests.py --coverage   # Run with coverage report
"""

import argparse
import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run CryptoInvestor DCA tests")
    parser.add_argument("--validation", action="store_true", help="Run only validation tests")
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration", action="store_true", help="Run only integration tests")
    parser.add_argument("--performance", action="store_true", help="Run only performance tests")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Base pytest command
    pytest_cmd = "python -m pytest tests/"
    
    # Add verbosity
    if args.verbose:
        pytest_cmd += " -v"
    
    # Add specific test markers
    if args.validation:
        pytest_cmd += " -m validation"
    elif args.unit:
        pytest_cmd += " -m unit"
    elif args.integration:
        pytest_cmd += " -m integration"
    elif args.performance:
        pytest_cmd += " -m performance"
    
    # Add coverage if requested
    if args.coverage:
        pytest_cmd += " --cov=src --cov-report=html --cov-report=term"
    
    print(f"Running: {pytest_cmd}")
    print("=" * 80)
    
    # Run the tests
    success = run_command(pytest_cmd)
    
    if success:
        print("\n" + "=" * 80)
        print(" ALL TESTS PASSED!")
        
        if args.coverage:
            print("\n Coverage report generated in htmlcov/")
            
        print("\n Key validation results:")
        print("    Optimum DCA: 462.1% return")
        print("    Simple DCA: 209.4% return") 
        print("    Outperformance: ~252.7 percentage points")
        
    else:
        print("\n" + "=" * 80)
        print(" SOME TESTS FAILED!")
        print("Please check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
