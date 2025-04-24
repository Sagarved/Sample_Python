import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import pandas as pd

# Function to fetch financial data
def fetch_financial_data():
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

        # Extract relevant data
        data = {
            "Current Assets": balance_sheet.loc["Total Current Assets"] if "Total Current Assets" in balance_sheet.index else pd.Series(),
            "Current Liabilities": balance_sheet.loc["Total Current Liabilities"] if "Total Current Liabilities" in balance_sheet.index else pd.Series(),
            "Inventory Sales (Revenues)": financials.loc["Total Revenue"] if "Total Revenue" in financials.index else pd.Series(),
            "COGS": financials.loc["Cost Of Revenue"] if "Cost Of Revenue" in financials.index else pd.Series(),
            "Account Receivable": balance_sheet.loc["Net Receivables"] if "Net Receivables" in balance_sheet.index else pd.Series(),
            "Net Fixed Assets": balance_sheet.loc["Property Plant Equipment"] if "Property Plant Equipment" in balance_sheet.index else pd.Series(),
            "Total Assets": balance_sheet.loc["Total Assets"] if "Total Assets" in balance_sheet.index else pd.Series(),
            "Total Liabilities": balance_sheet.loc["Total Liab"] if "Total Liab" in balance_sheet.index else pd.Series(),
            "EBIT": financials.loc["Ebit"] if "Ebit" in financials.index else pd.Series(),
            "Interest": financials.loc["Interest Expense"] if "Interest Expense" in financials.index else pd.Series(),
            "Depreciation": cashflow.loc["Depreciation"] if "Depreciation" in cashflow.index else pd.Series(),
            "Net Income": financials.loc["Net Income"] if "Net Income" in financials.index else pd.Series(),
            "Long Term Debt": balance_sheet.loc["Long Term Debt"] if "Long Term Debt" in balance_sheet.index else pd.Series(),
            "Notes Payable": balance_sheet.loc["Short Long Term Debt"] if "Short Long Term Debt" in balance_sheet.index else pd.Series(),
            "Common Equity": balance_sheet.loc["Common Stock"] if "Common Stock" in balance_sheet.index else pd.Series(),
            "Tax": financials.loc["Income Tax Expense"] if "Income Tax Expense" in financials.index else pd.Series(),
            "Total Debt": balance_sheet.loc["Total Debt"] if "Total Debt" in balance_sheet.index else pd.Series(),
        }
        print(data)
        # Clear the table
        for row in table.get_children():
            table.delete(row)

        # Populate the table with data
        for key, values in data.items():
            table.insert("", "end", values=[key] + list(values))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

# Create the main window
root = tk.Tk()
root.title("GUI-Based Ratio Analysis")

# Create input field for ticker symbol
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Ticker Symbol:").grid(row=0, column=0, padx=5)
ticker_entry = tk.Entry(frame)
ticker_entry.grid(row=0, column=1, padx=5)

fetch_button = tk.Button(frame, text="Fetch Financial Data", command=fetch_financial_data)
fetch_button.grid(row=0, column=2, padx=5)

# Create a table to display financial data
columns = ["Metric"] + ["Q1", "Q2", "Q3", "Q4"]  # Example columns for quarterly data
table = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack(pady=10)

# Run the application
root.mainloop()