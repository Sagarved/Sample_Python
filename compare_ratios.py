import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv('data.csv')

# Extract the list of companies and ratios
companies = data['Company']
ratios = data.columns[1:]  # Assuming first column is 'Company'

# Plot each ratio in a separate line graph
for ratio in ratios:
    plt.figure(figsize=(10, 6))
    plt.plot(companies, data[ratio], marker='o', label=ratio)
    plt.title(f'{ratio} Comparison Across Companies')
    plt.xlabel('Companies')
    plt.ylabel(ratio)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{ratio}_comparison.png')  # Save each graph as a PNG file
    plt.show()