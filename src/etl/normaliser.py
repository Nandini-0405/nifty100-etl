import pandas as pd

def normalize_year(df, column):
    df[column] = pd.to_datetime(df[column]).dt.year
    return df

def normalize_ticker(df, column):
    df[column] = df[column].str.upper().str.strip()
    return df