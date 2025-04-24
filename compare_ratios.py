import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
apple_data = pd.read_csv('/Users/P2982820/Co_Pilot/Sample_Python/GUI_based_Ratio_Analysis/logs/Apple Inc._ratios.csv', index_col=0)
alphabet_data = pd.read_csv('/Users/P2982820/Co_Pilot/Sample_Python/GUI_based_Ratio_Analysis/logs/Alphabet Inc._ratios.csv', index_col=0)

# Transpose the data for easier plotting
apple_data = apple_data.T
alphabet_data = alphabet_data.T

# Extract the list of ratios
ratios = apple_data.columns

# Plot each ratio in a separate line graph
for ratio in ratios:
    plt.figure(figsize=(10, 6))
    plt.plot(apple_data.index, apple_data[ratio], marker='o', label='Apple Inc.')
    plt.plot(alphabet_data.index, alphabet_data[ratio], marker='o', label='Alphabet Inc.')
    plt.title(f'{ratio} Comparison Between Apple Inc. and Alphabet Inc.')
    plt.xlabel('Year')
    plt.ylabel(ratio)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{ratio}_comparison.png')  # Save each graph as a PNG file
    plt.show()