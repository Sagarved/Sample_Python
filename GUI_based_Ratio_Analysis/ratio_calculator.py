import pandas as pd

def calculate_ratios(data):
    ratios = {}

    try:
        # Extract necessary data
        current_assets = data.get("Current Assets", pd.Series())
        current_liabilities = data.get("Current Liabilities", pd.Series())
        inventory = data.get("Inventory", pd.Series())
        total_assets = data.get("Total Assets", pd.Series())
        total_liabilities = data.get("Total Liabilities Net Minority Interest", pd.Series())
        total_revenue = data.get("Total Revenue", pd.Series())
        cogs = data.get("Cost Of Revenue", pd.Series())
        net_income = data.get("Net Income", pd.Series())
        ebit = data.get("EBIT", pd.Series())
        interest = data.get("Net Interest Income", pd.Series())
        common_equity = data.get("Common Stock Equity", pd.Series())

        # Calculate ratios for each period
        ratios["Current Ratio"] = current_assets / current_liabilities
        ratios["Quick Ratio"] = (current_assets - inventory) / current_liabilities
        ratios["Total Asset Turnover"] = total_revenue / total_assets
        ratios["Times Interest Earned"] = ebit / interest
        ratios["Gross Profit Margin"] = (total_revenue - cogs) / total_revenue
        ratios["Net Profit Margin"] = net_income / total_revenue
        ratios["Return on Total Assets"] = net_income / total_assets
        ratios["Return on Equity"] = net_income / common_equity
        ratios["Financial Leverage Multiplier"] = total_assets / common_equity

    except Exception as e:
        print(f"Error calculating ratios: {e}")

    return ratios