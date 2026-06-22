import pandas as pd

files = [
    "stock_prices.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx"
]

for file in files:
    print("\n================")
    print(file)

    df = pd.read_excel(f"data/raw/{file}")

    print(df.columns.tolist())