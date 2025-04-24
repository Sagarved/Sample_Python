import pandas as pd

def calculate_ratios(data, company_name):
    try:
        # Ensure all required columns are present
        required_columns = [
            "Current Assets", "Current Liabilities", "Inventory", "Total Assets",
            "Total Liabilities Net Minority Interest", "Total Revenue", "Cost Of Revenue",
            "Net Income", "EBIT", "Net Interest Income", "Common Stock Equity"
        ]
        

        # Extract data for calculations
        current_assets = data.loc["Current Assets"]
        current_liabilities = data.loc["Current Liabilities"]
        inventory = data.loc["Inventory Sales (Revenues)"]
        total_assets = data.loc["Total Assets"]
        total_liabilities = data.loc["Total Liabilities"]
        total_revenue = data.loc["Inventory Sales (Revenues)"]
        cogs = data.loc["COGS"]
        net_income = data.loc["Net Income"]
        ebit = data.loc["EBIT"]
        interest = data.loc["Interest"]
        common_equity = data.loc["Common Equity"]

        # Calculate ratios for each period
        ratios = pd.DataFrame({
            "Current Ratio": current_assets / current_liabilities,
            #"Quick Ratio": (current_assets - inventory) / current_liabilities,
            "Total Asset Turnover": total_revenue / total_assets,
            #"Times Interest Earned": ebit / interest,
            "Gross Profit Margin": (total_revenue - cogs) / total_revenue,
            "Net Profit Margin": net_income / total_revenue,
            "Return on Total Assets": net_income / total_assets,
            "Return on Equity": net_income / common_equity,
            "Financial Leverage Multiplier": total_assets / common_equity
        }).T

        # Display ratios on the terminal
        # print(ratios)
        # Save ratios to CSV files
        ratios.to_csv(f"logs/{company_name}_ratios.csv")

        return ratios

    except Exception as e:
        print(f"Error calculating ratios: {e}")
        return None