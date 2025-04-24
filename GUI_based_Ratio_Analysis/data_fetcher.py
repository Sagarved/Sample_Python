import yfinance as yf
import pandas as pd
from tkinter import messagebox

from ratio_calculator import calculate_ratios

def fetch_financial_data(ticker_entry, table, update_columns, update_ratios):
    ticker_symbol = ticker_entry.get().strip()
    if not ticker_symbol:
        messagebox.showerror("Error", "Please enter a ticker symbol.")
        return

    try:
        # Fetch financial data using yfinance
        stock = yf.Ticker(ticker_symbol)
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        # Extract company name
        company_name = stock.info.get("shortName", ticker_symbol)

      
        # Extract periods dynamically
        periods = list(balance_sheet.columns.strftime('%Y-%m-%d'))

        # Update table columns dynamically
        update_columns(periods)

        # Extract relevant data into a pandas DataFrame
        data = pd.DataFrame({
            "Current Assets": balance_sheet.loc["Current Assets"] if "Current Assets" in balance_sheet.index else pd.Series(),
            "Current Liabilities": balance_sheet.loc["Current Liabilities"] if "Current Liabilities" in balance_sheet.index else pd.Series(),
            "Inventory Sales (Revenues)": financials.loc["Total Revenue"] if "Total Revenue" in financials.index else pd.Series(),
            "COGS": financials.loc["Cost Of Revenue"] if "Cost Of Revenue" in financials.index else pd.Series(),
            "Account Receivable": balance_sheet.loc["Accounts Receivable"] if "Accounts Receivable" in balance_sheet.index else pd.Series(),
            "Net Fixed Assets": balance_sheet.loc["Total Non Current Assets"] if "Total Non Current Assets" in balance_sheet.index else pd.Series(),
            "Total Assets": balance_sheet.loc["Total Assets"] if "Total Assets" in balance_sheet.index else pd.Series(),
            "Total Liabilities": balance_sheet.loc["Total Liabilities Net Minority Interest"] if "Total Liabilities Net Minority Interest" in balance_sheet.index else pd.Series(),
            "EBIT": financials.loc["EBIT"] if "EBIT" in financials.index else pd.Series(),
            "Interest": financials.loc["Net Interest Income"] if "Net Interest Income" in financials.index else pd.Series(),
            "Net Income": financials.loc["Net Income"] if "Net Income" in financials.index else pd.Series(),
            "Common Equity": balance_sheet.loc["Common Stock Equity"] if "Common Stock Equity" in balance_sheet.index else pd.Series(),
        }).T  # Transpose to make keys as row indices

        # Save all fields to CSV files
        data.to_csv(f"logs/{company_name}_financial_data.csv")

        # Clear the table
        for row in table.get_children():
            table.delete(row)

        # Populate the table with data
        for index, row in data.iterrows():
            table.insert("", "end", values=[index] + list(row.values))

        # Debugging: Print data to ensure correctness
        print("Data for Ratios:", data)

        # Calculate and update ratios
        ratio_data = calculate_ratios(data)

        # Debugging: Print calculated ratios to ensure correctness
        print("Calculated Ratios:", ratio_data)

        update_ratios(periods, ratio_data)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")