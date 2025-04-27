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
    all_periods = {"annual": set(), "quarterly": set()}

    for ticker_symbol in tickers:
        ticker_symbol = ticker_symbol.strip()
        if not ticker_symbol:
            continue

        try:
            # Fetch financial data using yfinance
            stock = yf.Ticker(ticker_symbol)
            financials_annual = stock.financials
            balance_sheet_annual = stock.balance_sheet
            cashflow_annual = stock.cashflow

            financials_quarterly = stock.quarterly_financials
            balance_sheet_quarterly = stock.quarterly_balance_sheet
            cashflow_quarterly = stock.quarterly_cashflow

            # Extract company name
            company_name = stock.info.get("shortName", ticker_symbol)

            # Extract periods dynamically
            periods_annual = list(balance_sheet_annual.columns.strftime('%Y-%m-%d'))
            periods_quarterly = list(balance_sheet_quarterly.columns.strftime('%Y-%m-%d'))
            all_periods["annual"].update(periods_annual)
            all_periods["quarterly"].update(periods_quarterly)

            # Extract relevant data into pandas DataFrames for annual and quarterly
            def extract_data(balance_sheet, financials, periods):
                return pd.DataFrame({
                    "Current Assets": balance_sheet.loc["Current Assets"] if "Current Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Current Liabilities": balance_sheet.loc["Current Liabilities"] if "Current Liabilities" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Inventory": balance_sheet.loc["Inventory"] if "Inventory" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Inventory Sales (Revenues)": financials.loc["Total Revenue"] if "Total Revenue" in financials.index else pd.Series(index=periods, dtype='float64'),
                    "COGS": financials.loc["Cost Of Revenue"] if "Cost Of Revenue" in financials.index else pd.Series(index=periods, dtype='float64'),
                    "Account Receivable": balance_sheet.loc["Accounts Receivable"] if "Accounts Receivable" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Net Fixed Assets": balance_sheet.loc["Total Non Current Assets"] if "Total Non Current Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Total Assets": balance_sheet.loc["Total Assets"] if "Total Assets" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "Total Liabilities": balance_sheet.loc["Total Liabilities Net Minority Interest"] if "Total Liabilities Net Minority Interest" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                    "EBIT": financials.loc["Operating Income"] if "Operating Income" in financials.index else pd.Series(index=periods, dtype='float64'),
                    "Net Income": financials.loc["Net Income"] if "Net Income" in financials.index else pd.Series(index=periods, dtype='float64'),
                    "Common Equity": balance_sheet.loc["Common Stock Equity"] if "Common Stock Equity" in balance_sheet.index else pd.Series(index=periods, dtype='float64'),
                }).fillna(0).T  # Transpose to make keys as row indices and fill missing values with 0

            data_annual = extract_data(balance_sheet_annual, financials_annual, periods_annual)
            data_quarterly = extract_data(balance_sheet_quarterly, financials_quarterly, periods_quarterly)

            # Calculate and store ratios for annual and quarterly data
            ratio_data_annual = calculate_ratios(data_annual, company_name)
            ratio_data_quarterly = calculate_ratios(data_quarterly, company_name)
            # store the data in csv file
            # data_annual.to_csv(f"logs/{company_name}_annual_financial_data.csv", index=True)
            # data_quarterly.to_csv(f"logs/{company_name}_quarterly_financial_data.csv", index=True)
            all_ratios[company_name] = {
                "annual": ratio_data_annual,
                "quarterly": ratio_data_quarterly
            }

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data for {ticker_symbol}: {e}")

    # Update columns and ratios in the GUI
    update_columns({"annual": sorted(all_periods["annual"]), "quarterly": sorted(all_periods["quarterly"])} )
    update_ratios(all_ratios)