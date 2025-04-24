import tkinter as tk
from tkinter import ttk, messagebox
from data_fetcher import fetch_financial_data
from ratio_calculator import calculate_ratios

# Create the main window
root = tk.Tk()
root.title("GUI-Based Ratio Analysis")

# Create input field for ticker symbol
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Enter Ticker Symbol:").grid(row=0, column=0, padx=5)
ticker_entry = tk.Entry(frame)
ticker_entry.grid(row=0, column=1, padx=5)

fetch_button = tk.Button(frame, text="Fetch Financial Data", command=lambda: fetch_financial_data(ticker_entry, table, update_columns, update_ratios))
fetch_button.grid(row=0, column=2, padx=5)

# Create a table to display financial data
columns = ["Metric"]  # Initial columns, will be updated dynamically
table = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack(pady=10)

# Create a table to display financial ratios
ratio_columns = ["Metric"]  # Initial columns, will be updated dynamically
ratio_table = ttk.Treeview(root, columns=ratio_columns, show="headings", height=10)
for col in ratio_columns:
    ratio_table.heading(col, text=col)
    ratio_table.column(col, width=150)

ratio_table.pack(pady=10)

# Function to update table columns dynamically
def update_columns(periods):
    table["columns"] = ["Metric"] + periods
    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, width=150)

# Function to update ratio table dynamically
def update_ratios(periods, ratio_data):
    ratio_table["columns"] = ["Metric"] + periods
    for col in ratio_table["columns"]:
        ratio_table.heading(col, text=col)
        ratio_table.column(col, width=150)

    # Clear the ratio table
    for row in ratio_table.get_children():
        ratio_table.delete(row)

    # Populate the ratio table with data
    for ratio, values in ratio_data.iterrows():
        ratio_table.insert("", "end", values=[ratio] + list(values.values))

# Run the application
root.mainloop()