import yfinance as yf
import pandas as pd

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    return stock.info, stock.financials, stock.balance_sheet, stock.cashflow

def calculate_roe(net_income, shareholder_equity):
    return net_income / shareholder_equity

def calculate_current_ratio(current_assets, current_liabilities):
    return current_assets / current_liabilities

def calculate_quick_ratio(current_assets, inventory, current_liabilities):
    return (current_assets - inventory) / current_liabilities

def calculate_debt_to_equity_ratio(total_liabilities, shareholder_equity):
    return total_liabilities / shareholder_equity

def calculate_roa(net_income, total_assets):
    return net_income / total_assets

def analyze_company(ticker):
    info, financials, balance_sheet, cashflow = get_financial_data(ticker)
    if info is None:
        return None
    # Calculate key metrics
    print(f"Analyzing {info['shortName']} ({ticker})")
    print("Financial Data:")
    print(financials)
    print(balance_sheet)
    print(cashflow)
    roe = calculate_roe(financials.loc['Net Income'], balance_sheet.loc['Total Stockholder Equity']
    pe_ratio = info['forwardPE']
    
    current_ratio = calculate_current_ratio(balance_sheet.loc['Total Current Assets'].iloc[0], balance_sheet.loc['Total Current Liabilities'].iloc[0])
    quick_ratio = calculate_quick_ratio(balance_sheet.loc['Total Current Assets'].iloc[0], balance_sheet.loc['Inventory'].iloc[0], balance_sheet.loc['Total Current Liabilities'].iloc[0])
    debt_to_equity_ratio = calculate_debt_to_equity_ratio(balance_sheet.loc['Total Liab'].iloc[0], balance_sheet.loc['Total Stockholder Equity'].iloc[0])
    roa = calculate_roa(financials.loc['Net Income'].iloc[0], balance_sheet.loc['Total Assets'].iloc[0])
    
    return {
        'ROE': roe,
        'P/B Ratio': pb_ratio,
        'P/E Ratio': pe_ratio,
        'Current Ratio': current_ratio,
        'Quick Ratio': quick_ratio,
        'Debt to Equity Ratio': debt_to_equity_ratio,
        'ROA': roa,
    }

def compare_companies(ticker1, ticker2):
    analysis1 = analyze_company(ticker1)
    analysis2 = analyze_company(ticker2)
    
    if analysis1 is None or analysis2 is None:
        print("Error in fetching data for one of the companies.")
        return
    
    print(f"Comparison between {ticker1} and {ticker2}:")
    for key in analysis1.keys():
        print(f"{key}: {ticker1} = {analysis1[key]}, {ticker2} = {analysis2[key]}")
        # Add comments for each ratio from Warren Buffett's perspective
        if key == 'ROE':
            print("ROE (Return on Equity): Warren Buffett prefers companies with ROE consistently above 15%.")
        elif key == 'P/B Ratio':
            print("P/B Ratio (Price to Book): A lower P/B ratio may indicate undervaluation, but Buffett looks for quality companies even if P/B is higher.")
        elif key == 'P/E Ratio':
            print("P/E Ratio (Price to Earnings): Buffett prefers companies with a reasonable P/E ratio relative to their growth prospects.")
        elif key == 'Current Ratio':
            print("Current Ratio: Buffett looks for companies with a strong liquidity position, typically a current ratio above 1.5.")
        elif key == 'Quick Ratio':
            print("Quick Ratio: Similar to the current ratio, but excludes inventory. Buffett prefers a quick ratio above 1.")
        elif key == 'Debt to Equity Ratio':
            print("Debt to Equity Ratio: Buffett prefers companies with low debt levels, typically a debt to equity ratio below 0.5.")
        elif key == 'ROA':
            print("ROA (Return on Assets): Buffett looks for companies with a high ROA, indicating efficient use of assets.")

# Example usage
compare_companies('AAPL', 'MSFT')
