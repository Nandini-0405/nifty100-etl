import pandas as pd

def load_excel(file_path):
    df = pd.read_excel(file_path)
    return df

if __name__ == "__main__":
    df = load_excel("data/sample.xlsx")
    print(df.head())