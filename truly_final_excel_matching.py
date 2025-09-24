#!/usr/bin/env python3
"""
TRULY FINAL Excel-Matching DCA Implementation

Uses the actual Investment Multiple and Buy/Sell Multiplier values 
directly from the main '20222023 WDCA' sheet with correct dates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class WeeklyRecord:
    """Record for a single week's DCA activity."""
    date: date
    btc_price: float
    investment_amount: float
    btc_purchased: float
    total_btc_units: float
    total_investment: float
    avg_buy_price: float
    current_value: float
    profit_loss: float
    profit_loss_pct: float
    capital_balance: float
    action: str
    notes: str = ""

class SimpleDCAWeekly:
    """Simple Weekly DCA: $250 every Monday."""
    
    def __init__(self, total_capital: float = 48500.0):
        self.weekly_budget = 250.0
        self.total_capital = total_capital
        self.total_btc_units = 0.0
        self.total_investment = 0.0
        self.capital_balance = total_capital
        self.records: List[WeeklyRecord] = []
    
    def process_week(self, monday_date: date, btc_price: float) -> WeeklyRecord:
        """Process a single week's DCA investment."""
        if self.capital_balance >= self.weekly_budget:
            investment_amount = self.weekly_budget
            self.capital_balance -= investment_amount
        else:
            investment_amount = self.capital_balance
            self.capital_balance = 0
        
        if investment_amount > 0:
            btc_purchased = investment_amount / btc_price
            self.total_btc_units += btc_purchased
            self.total_investment += investment_amount
            action = 'BUY'
        else:
            btc_purchased = 0
            action = 'HOLD'
        
        avg_buy_price = self.total_investment / self.total_btc_units if self.total_btc_units > 0 else 0
        current_value = self.total_btc_units * btc_price
        profit_loss = current_value - self.total_investment
        profit_loss_pct = (profit_loss / self.total_investment * 100) if self.total_investment > 0 else 0
        
        record = WeeklyRecord(
            date=monday_date,
            btc_price=btc_price,
            investment_amount=investment_amount,
            btc_purchased=btc_purchased,
            total_btc_units=self.total_btc_units,
            total_investment=self.total_investment,
            avg_buy_price=avg_buy_price,
            current_value=current_value,
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            capital_balance=self.capital_balance,
            action=action
        )
        
        self.records.append(record)
        return record

class TrulyFinalOptimumDCA:
    """TRULY FINAL Excel Optimum DCA using values from main DCA sheet."""
    
    def __init__(self, total_capital: float = 48500.0):
        self.weekly_budget = 250.0
        self.total_capital = total_capital
        self.total_btc_units = 0.0
        self.net_investment = 0.0  # Track net investment like Excel
        self.capital_balance = total_capital
        self.records: List[WeeklyRecord] = []
        self.excel_dca_data = None
        self.unlimited_capital = True  # Excel appears to have unlimited capital for strategy
    
    def load_excel_dca_data(self):
        """Load the exact Investment Multiple data from main '20222023 WDCA' sheet."""
        df_excel = pd.read_excel("Optimum DCA clubhouse.xlsx", sheet_name="20222023 WDCA", header=1)
        
        # Filter valid dates only (remove summary rows)
        date_mask = df_excel['Trade Date'].astype(str).str.contains(r'\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{4}|\d{1,2}-\d{1,2}-\d{4}', na=False)
        df_excel_clean = df_excel[date_mask].copy()
        df_excel_clean['Trade Date'] = pd.to_datetime(df_excel_clean['Trade Date']).dt.date
        
        # Set date as index for easy lookup
        self.excel_dca_data = df_excel_clean.set_index('Trade Date')
        
        print(f"Loaded {len(self.excel_dca_data)} weeks of Excel DCA data")
        print(f"Date range: {df_excel_clean['Trade Date'].min()} to {df_excel_clean['Trade Date'].max()}")
        
        # Verify total investment matches
        total_inv = df_excel_clean['Investment Amount Optimum scenario'].sum()
        print(f"Total Excel investment: ${total_inv:,.2f}")
        
        # Show first few rows to verify
        print("\nFirst 5 weeks of Excel DCA data:")
        for i, (date_idx, row) in enumerate(self.excel_dca_data.head().iterrows()):
            inv_mult = row.get('Investment Multiple Optimum scenario', 'N/A')
            bs_mult = row.get('Buy/Sell Multiplier', 'N/A')
            inv_amount = row.get('Investment Amount Optimum scenario', 'N/A')
            print(f"  {date_idx}: InvMult={inv_mult:.3f}, BS={bs_mult}, Amount=${inv_amount:.2f}")
    
    def get_excel_investment_signals(self, monday_date: date) -> tuple:
        """Get exact Investment Multiple and Buy/Sell Multiplier from Excel DCA data."""
        if self.excel_dca_data is None or monday_date not in self.excel_dca_data.index:
            return 1.0, 0, 250.0  # Default fallback
        
        row = self.excel_dca_data.loc[monday_date]
        
        investment_multiple = row.get('Investment Multiple Optimum scenario', 1.0)
        buy_sell_multiplier = row.get('Buy/Sell Multiplier', 0)
        investment_amount = row.get('Investment Amount Optimum scenario', 250.0)
        
        # Handle NaN/None values
        if pd.isna(investment_multiple) or investment_multiple is None:
            investment_multiple = 1.0
        if pd.isna(buy_sell_multiplier) or buy_sell_multiplier is None:
            buy_sell_multiplier = 0
        if pd.isna(investment_amount) or investment_amount is None:
            investment_amount = 250.0
        
        return investment_multiple, buy_sell_multiplier, investment_amount
    
    def process_week(self, monday_date: date, btc_price: float) -> WeeklyRecord:
        """Process a single week using EXACT Excel data."""
        investment_multiple, buy_sell_multiplier, excel_investment_amount = self.get_excel_investment_signals(monday_date)
        
        # Use the EXACT investment amount from Excel (not a calculation)
        raw_investment = excel_investment_amount
        
        # Process the investment using exact Excel amounts
        if raw_investment > 0:
            # Buying - use exact Excel amount (Excel may have unlimited capital access)
            investment_amount = raw_investment
            if self.unlimited_capital or investment_amount <= self.capital_balance:
                btc_purchased = investment_amount / btc_price
                self.total_btc_units += btc_purchased
                self.net_investment += investment_amount  # Add to net investment
                self.capital_balance -= investment_amount
                action = 'BUY'
                notes = f"Excel: InvMult={investment_multiple:.3f}, BS={buy_sell_multiplier}, Amount=${excel_investment_amount:.0f}"
            else:
                # Limited capital - buy what we can
                investment_amount = self.capital_balance
                if investment_amount > 0:
                    btc_purchased = investment_amount / btc_price
                    self.total_btc_units += btc_purchased
                    self.net_investment += investment_amount  # Add to net investment
                    self.capital_balance = 0
                    action = 'BUY'
                    notes = f"Limited capital: ${investment_amount:.0f} of ${raw_investment:.0f} requested"
                else:
                    btc_purchased = 0
                    investment_amount = 0
                    action = 'HOLD'
                    notes = "No capital available"
        
        elif raw_investment < 0:
            # Selling (negative investment amount) - use exact Excel selling amount
            sell_value = abs(raw_investment)
            btc_to_sell = sell_value / btc_price
            
            if btc_to_sell <= self.total_btc_units:
                # Execute the exact sell as specified by Excel
                self.total_btc_units -= btc_to_sell
                self.capital_balance += sell_value
                
                # Excel net investment tracking: subtract the selling amount (which is negative)
                self.net_investment += raw_investment  # raw_investment is negative, so this reduces net_investment
                
                investment_amount = raw_investment  # Keep negative for reporting
                btc_purchased = -btc_to_sell       # Negative for sold
                action = 'SELL'
                notes = f"Excel: Sold ${sell_value:.0f} worth ({btc_to_sell:.6f} BTC)"
            else:
                # Excel wants to sell more than we have - this shouldn't happen with correct data
                investment_amount = 0
                btc_purchased = 0
                action = 'HOLD'
                notes = f"Excel sell error: want ${sell_value:.0f}, only have {self.total_btc_units:.6f} BTC"
        else:
            # Zero investment
            investment_amount = 0
            btc_purchased = 0
            action = 'HOLD'
            notes = f"Neutral: {investment_multiple:.3f}"
        
        # Calculate metrics using Excel's net investment approach
        avg_buy_price = self.net_investment / self.total_btc_units if self.total_btc_units > 0 and self.net_investment > 0 else 0
        current_value = self.total_btc_units * btc_price
        profit_loss = current_value - self.net_investment
        profit_loss_pct = (profit_loss / self.net_investment * 100) if self.net_investment > 0 else 0
        
        record = WeeklyRecord(
            date=monday_date,
            btc_price=btc_price,
            investment_amount=investment_amount,
            btc_purchased=btc_purchased,
            total_btc_units=self.total_btc_units,
            total_investment=self.net_investment,  # Use net investment for Excel matching
            avg_buy_price=avg_buy_price,
            current_value=current_value,
            profit_loss=profit_loss,
            profit_loss_pct=profit_loss_pct,
            capital_balance=self.capital_balance,
            action=action,
            notes=notes
        )
        
        self.records.append(record)
        return record

class TrulyFinalComparison:
    """Truly final DCA comparison using exact Excel data from main DCA sheet."""
    
    def __init__(self, start_date: str = "2022-01-10", end_date: str = "2025-09-22"):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # Calculate weeks and total capital
        start_monday = self.start_date
        while start_monday.weekday() != 0:  # Ensure Monday
            start_monday += timedelta(days=1)
        
        end_monday = self.end_date
        while end_monday.weekday() != 0:  # Ensure Monday
            end_monday -= timedelta(days=1)
        
        self.weeks = ((end_monday - start_monday).days // 7) + 1
        self.total_capital = self.weeks * 250  # $250 per week
        
        self.simple_dca = SimpleDCAWeekly(self.total_capital)
        self.optimum_dca = TrulyFinalOptimumDCA(self.total_capital)
        
        self.price_data = None
        self.comparison_results = []
    
    def load_price_data(self, csv_path: str = "data/bitcoin_prices.csv"):
        """Load Bitcoin price data."""
        df = pd.read_csv(csv_path)
        
        # Clean the data
        df['date'] = pd.to_datetime(df['date'], format='%m-%d-%Y').dt.date
        df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float)
        df = df.dropna(subset=['Price'])
        df = df.sort_values('date').reset_index(drop=True)
        
        self.price_data = df
        print(f"Loaded {len(df)} days of valid price data from {df['date'].min()} to {df['date'].max()}")
        
        return df
    
    def generate_monday_dates(self):
        """Generate Monday dates for the comparison period."""
        mondays = []
        current_date = self.start_date
        
        # Ensure we start on a Monday
        while current_date.weekday() != 0:
            current_date += timedelta(days=1)
        
        # Generate Mondays until end date
        while current_date <= self.end_date:
            mondays.append(current_date)
            current_date += timedelta(days=7)
        
        return mondays
    
    def get_price_for_date(self, target_date: date) -> float:
        """Get Bitcoin price for a specific date."""
        exact_match = self.price_data[self.price_data['date'] == target_date]
        if not exact_match.empty:
            return float(exact_match['Price'].iloc[0])
        
        # Find closest date before target
        before_dates = self.price_data[self.price_data['date'] <= target_date]
        if not before_dates.empty:
            return float(before_dates['Price'].iloc[-1])
        
        # If no date before, use first available
        return float(self.price_data['Price'].iloc[0])
    
    def run_comparison(self):
        """Run the truly final comparison."""
        if self.price_data is None:
            raise ValueError("Price data not loaded.")
        
        print("Loading Excel DCA data from main sheet...")
        self.optimum_dca.load_excel_dca_data()
        
        # Generate Monday dates
        mondays = self.generate_monday_dates()
        
        print(f"\nRunning TRULY FINAL comparison:")
        print(f"  Start: {self.start_date}")
        print(f"  End: {self.end_date}")
        print(f"  Total weeks: {len(mondays)}")
        print(f"  Total capital: ${self.total_capital:,.0f}")
        
        # Process each Monday
        for i, monday in enumerate(mondays):
            btc_price = self.get_price_for_date(monday)
            
            # Process both strategies
            simple_record = self.simple_dca.process_week(monday, btc_price)
            optimum_record = self.optimum_dca.process_week(monday, btc_price)
            
            # Store comparison
            self.comparison_results.append({
                'date': monday,
                'btc_price': btc_price,
                'simple': simple_record,
                'optimum': optimum_record
            })
            
            if i % 20 == 0:
                print(f"  Processed {i+1}/{len(mondays)} weeks...")
        
        print("TRULY FINAL comparison completed!")
    
    def generate_summary_report(self) -> str:
        """Generate truly final summary report."""
        if not self.comparison_results:
            return "No results available."
        
        final_simple = self.comparison_results[-1]['simple']
        final_optimum = self.comparison_results[-1]['optimum']
        final_price = self.comparison_results[-1]['btc_price']
        
        total_weeks = len(self.comparison_results)
        
        report = []
        report.append("=" * 80)
        report.append("🎯 TRULY FINAL EXCEL-MATCHING BITCOIN DCA COMPARISON 🎯")
        report.append("=" * 80)
        report.append(f"Period: {self.start_date} to {self.end_date}")
        report.append(f"Total Weeks: {total_weeks}")
        report.append(f"Total Capital: ${self.total_capital:,.0f}")
        report.append(f"Final BTC Price: ${final_price:,.2f}")
        report.append("")
        
        # Simple DCA Results
        report.append("📈 SIMPLE DCA RESULTS:")
        report.append("-" * 40)
        report.append(f"Total BTC: {final_simple.total_btc_units:.8f}")
        report.append(f"Invested: ${final_simple.total_investment:,.2f}")
        report.append(f"Avg Price: ${final_simple.avg_buy_price:,.2f}")
        report.append(f"Current Value: ${final_simple.current_value:,.2f}")
        report.append(f"Profit: ${final_simple.profit_loss:,.2f} ({final_simple.profit_loss_pct:.1f}%)")
        report.append(f"Capital Left: ${final_simple.capital_balance:,.2f}")
        report.append("")
        
        # Truly Final Optimum DCA Results
        report.append("🎯 TRULY FINAL OPTIMUM DCA RESULTS:")
        report.append("-" * 40)
        report.append(f"Total BTC: {final_optimum.total_btc_units:.8f}")
        report.append(f"Net Invested: ${final_optimum.total_investment:,.2f}")
        report.append(f"Avg Price: ${final_optimum.avg_buy_price:,.2f}")
        report.append(f"Current Value: ${final_optimum.current_value:,.2f}")
        report.append(f"Profit: ${final_optimum.profit_loss:,.2f} ({final_optimum.profit_loss_pct:.1f}%)")
        report.append(f"Capital Left: ${final_optimum.capital_balance:,.2f}")
        report.append("")
        
        # Compare with Excel target (462%)
        excel_target_return = 462.0
        excel_target_btc = 2.26488572
        excel_target_value = 263082.58
        
        actual_optimum_return = final_optimum.profit_loss_pct
        btc_match_ratio = final_optimum.total_btc_units / excel_target_btc
        value_match_ratio = final_optimum.current_value / excel_target_value
        
        report.append("🎯 EXCEL MATCH ANALYSIS:")
        report.append("-" * 40)
        report.append(f"Excel Target: {excel_target_btc:.8f} BTC, ${excel_target_value:,.2f} value, {excel_target_return:.1f}% return")
        report.append(f"My Result: {final_optimum.total_btc_units:.8f} BTC, ${final_optimum.current_value:,.2f} value, {actual_optimum_return:.1f}% return")
        report.append(f"BTC Match: {btc_match_ratio:.2f}x ({btc_match_ratio*100:.1f}%)")
        report.append(f"Value Match: {value_match_ratio:.2f}x ({value_match_ratio*100:.1f}%)")
        report.append(f"Return Match: {(actual_optimum_return / excel_target_return * 100):.1f}%")
        
        # Performance comparison
        if final_optimum.current_value > final_simple.current_value:
            diff = final_optimum.current_value - final_simple.current_value
            outperform_pct = (diff / final_simple.current_value * 100)
            report.append(f"\n🏆 WINNER: Truly Final Optimum DCA (+${diff:,.2f})")
            report.append(f"Optimum DCA outperformed by {outperform_pct:.1f}%")
        else:
            diff = final_simple.current_value - final_optimum.current_value
            report.append(f"\n🏆 WINNER: Simple DCA (+${diff:,.2f})")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def export_detailed_report(self, filename: str = "truly_final_excel_matching_dca.csv"):
        """Export detailed report."""
        detailed_data = []
        
        for result in self.comparison_results:
            simple = result['simple']
            optimum = result['optimum']
            
            detailed_data.append({
                'date': result['date'],
                'btc_price': result['btc_price'],
                'simple_investment': simple.investment_amount,
                'simple_btc': simple.total_btc_units,
                'simple_value': simple.current_value,
                'simple_profit_pct': simple.profit_loss_pct,
                'optimum_action': optimum.action,
                'optimum_investment': optimum.investment_amount,
                'optimum_btc': optimum.total_btc_units,
                'optimum_value': optimum.current_value,
                'optimum_profit_pct': optimum.profit_loss_pct,
                'optimum_notes': optimum.notes
            })
        
        df = pd.DataFrame(detailed_data)
        df.to_csv(filename, index=False)
        print(f"Truly final detailed report exported to {filename}")
        
        return df

def main():
    """Run the truly final comparison."""
    print("🎯 RUNNING TRULY FINAL EXCEL-MATCHING DCA COMPARISON")
    print("Using exact Investment Amount values from main '20222023 WDCA' sheet")
    
    comparison = TrulyFinalComparison(
        start_date="2022-01-10",
        end_date="2025-09-22"
    )
    
    # Load data and run comparison
    comparison.load_price_data()
    comparison.run_comparison()
    
    # Generate reports
    summary = comparison.generate_summary_report()
    print("\n" + summary)
    
    # Export detailed report
    detailed_df = comparison.export_detailed_report()

if __name__ == "__main__":
    main()
