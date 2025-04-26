import yfinance as yf
import pandas as pd
from tkinter import messagebox

from ratio_calculator import calculate_ratios

def fetch_financial_data(ticker_entry, table, update_columns, update_ratios):
    tickers = ticker_entry.get().strip().split(',')  # Allow multiple tickers separated by commas
    if not tickers:
        messagebox.showerror("Error", "Please enter at least one ticker symbol.")
        return

    all_ratios = {}
    all_periods = set()

    for ticker_symbol in tickers:
        ticker_symbol = ticker_symbol.strip()
        if not ticker_symbol:
            continue

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
            all_periods.update(periods)

            # Extract relevant data into a pandas DataFrame
            data = pd.DataFrame({
                "Current Assets": balance_sheet.loc["Current Assets"] if "Current Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "Current Liabilities": balance_sheet.loc["Current Liabilities"] if "Current Liabilities" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "Inventory": balance_sheet.loc["Inventory"] if "Inventory" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "Inventory Sales (Revenues)": financials.loc["Operating Revenue"] if "Operating Revenue" in financials.index else pd.Series(index=periods, dtype='float64'),
                "COGS": financials.loc["Cost Of Revenue"] if "Cost Of Revenue" in financials.index else pd.Series(index=periods, dtype='float64'),
                "Net Fixed Assets": balance_sheet.loc["Total Non Current Assets"] if "Total Non Current Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "Total Assets": balance_sheet.loc["Total Assets"] if "Total Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "Total Liabilities": balance_sheet.loc["Total Liabilities Net Minority Interest"] if "Total Liabilities Net Minority Interest" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                "EBIT": financials.loc["Operating Income"] if "Operating Income" in financials.index else pd.Series(index=periods, dtype='float64'),
                "Net Income": financials.loc["Net Income"] if "Net Income" in financials.index else pd.Series(index=periods, dtype='float64'),
                "Common Equity": balance_sheet.loc["Stockholders Equity"] if "Stockholders Equity" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
            }).T  # Transpose to make keys as row indices

            # Fill missing values with 0 for calculations
            # data = data.fillna(0)
            # store the data in csv file
            data.to_csv(f"logs/{company_name}_financial_data.csv", index=True)
            # Save the data to a CSV file
            """
            balance_sheet.to_csv(f"logs/{company_name}_balance_sheet.csv", index=True)
            financials.to_csv(f"logs/{company_name}_financials.csv", index=True)
            cashflow.to_csv(f"logs/{company_name}_cashflow.csv", index=True)
            """

            # Calculate and store ratios
            ratio_data = calculate_ratios(data, company_name)
            all_ratios[company_name] = ratio_data

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data for {ticker_symbol}: {e}")

    # Update columns and ratios in the GUI
    update_columns(sorted(all_periods))
    update_ratios(all_ratios)