import pandas as pd

def calculate_ratios(data, company_name):
    ratios = {}

    try:
        # Calculate various financial ratios
        for period in data.columns:
                ratios[period] = {
                    "Current Ratio": data.loc["Current Assets", period] / data.loc["Current Liabilities", period] if data.loc["Current Liabilities", period] != 0 else "N/A",
                    "Quick Ratio": (data.loc["Current Assets", period] - data.loc["Inventory", period]) / data.loc["Current Liabilities", period] if data.loc["Current Liabilities", period] != 0 else "N/A",
                    "Inventory Turnover": data.loc["Inventory Sales (Revenues)", period] / data.loc["Inventory", period] if data.loc["Inventory", period] != 0 else "N/A",
                    "Total Assets Turnover": data.loc["Inventory Sales (Revenues)", period] / data.loc["Total Assets", period] if data.loc["Total Assets", period] != 0 else "N/A",
                    "Return on Assets": data.loc["Net Income", period] / data.loc["Total Assets", period] if data.loc["Total Assets", period] != 0 else "N/A",
                    "Return on Equity": data.loc["Net Income", period] / data.loc["Common Equity", period] if data.loc["Common Equity", period] != 0 else "N/A",
                    "Gross Profit Margin": data.loc["EBIT", period] / data.loc["Inventory Sales (Revenues)", period] if data.loc["Inventory Sales (Revenues)", period] != 0 else "N/A",
                    "Net Profit Margin": data.loc["Net Income", period] / data.loc["Inventory Sales (Revenues)", period] if data.loc["Inventory Sales (Revenues)", period] != 0 else "N/A",

                }

        # store the ratios in a csv file
        # ratios_df = pd.DataFrame(ratios)
        #ratios_df= ratios_df.T  # Transpose to make keys as row indices
        #ratios_df.to_csv(f"logs/{company_name}_ratios_from_rc.csv", index=True)
        return ratios

    except Exception as e:
        raise ValueError(f"Error calculating ratios for {company_name}: {e}")