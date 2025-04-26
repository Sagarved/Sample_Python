from tkinter import Tk, Label, Entry, Button, Frame, Scrollbar, Canvas
from tkinter import ttk
import os
from data_fetcher import fetch_financial_data

def update_columns(periods):
    # Update the GUI to display periods dynamically
    pass

def update_ratios(all_ratios):
    # Clear existing sections
    for widget in ratio_frame.winfo_children():
        widget.destroy()

    for company, ratios in all_ratios.items():
        # Create a frame for each company
        company_frame = Frame(ratio_frame)
        company_frame.pack(fill="x", pady=(10, 20))

        # Add company name as title
        company_label = Label(company_frame, text=company, font=("Arial", 14, "bold"))
        company_label.pack(anchor="w", pady=(0, 10))

        # Create a table for ratios
        periods = list(next(iter(ratios.values())).keys())  # Extract periods (year and date)
        table = ttk.Treeview(company_frame, columns=["Ratio"] + periods, show="headings")
        table.pack(fill="x")

        # Set column headings
        table.heading("Ratio", text="Ratio")
        table.column("Ratio", width=150, anchor="center")
        for period in periods:
            table.heading(period, text=period)
            table.column(period, width=100, anchor="center")

        # Add rows for each ratio
        for ratio_name, ratio_values in ratios.items():
            row = [ratio_values.get(period, "N/A") for period in periods]
            table.insert("", "end", values=[ratio_name] + row)

       
# Initialize the main GUI window
root = Tk()
root.title("Financial Ratio Analysis")

# Input section
input_label = Label(root, text="Enter Ticker Symbols (comma-separated):")
input_label.pack(pady=(10, 0))

ticker_entry = Entry(root, width=50)
ticker_entry.pack(pady=(0, 10))

fetch_button = Button(root, text="Fetch Data", command=lambda: fetch_financial_data(ticker_entry, None, update_columns, update_ratios))
fetch_button.pack(pady=(0, 10))

# Scrollable frame for displaying ratios
canvas = Canvas(root)
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
ratio_frame = Frame(canvas)

ratio_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=ratio_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Update the scrollable frame to ensure scrolling works
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

# Start the GUI event loop
root.mainloop()