import pandas as pd

def calculate_ratios(data, company_name):
    try:
        # Calculate various financial ratios
        ratios = {
            "Current Ratio": data.loc["Current Assets"] / data.loc["Current Liabilities"],
            "Quick Ratio": (data.loc["Current Assets"] - data.loc["Inventory"]) / data.loc["Current Liabilities"],
            "Inventory Turnover": data.loc["Inventory Sales (Revenues)"] / data.loc["Inventory"],
            "Total Assets Turnover": data.loc["Inventory Sales (Revenues)"] / data.loc["Total Assets"],
            "Return on Assets": data.loc["Net Income"] / data.loc["Total Assets"],
            "Return on Equity": data.loc["Net Income"] / data.loc["Common Equity"],
            "Gross Profit Margin": (data.loc["EBIT"]) / data.loc["Inventory Sales (Revenues)"],
            "Net Profit Margin": data.loc["Net Income"] / data.loc["Inventory Sales (Revenues)"],
        }
        # store the ratios in a csv file
        ratios_df = pd.DataFrame(ratios)
        ratios_df= ratios_df.T  # Transpose to make keys as row indices
        ratios_df.to_csv(f"logs/{company_name}_ratios_from_rc.csv", index=True)
        # Return the calculated ratios
        return ratios
    except Exception as e:
        print(f"Error calculating ratios for {company_name}: {e}")
        return {}