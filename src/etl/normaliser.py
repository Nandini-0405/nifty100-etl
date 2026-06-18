import pandas as pd

def normalize_year(df, column="year"):
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].astype("Int64")
    return df

def normalize_ticker(df, column="ticker"):
    df[column] = df[column].astype(str).str.upper().str.strip()
    return df