import pandas as pd
from src.etl.normaliser import normalize_year, normalize_ticker

def test_year_integer():
    df = pd.DataFrame({"year":[2024]})
    assert normalize_year(df)["year"][0] == 2024

def test_year_string():
    df = pd.DataFrame({"year":["2023"]})
    assert normalize_year(df)["year"][0] == 2023

def test_ticker_upper():
    df = pd.DataFrame({"ticker":["tcs"]})
    assert normalize_ticker(df)["ticker"][0] == "TCS"

def test_ticker_spaces():
    df = pd.DataFrame({"ticker":[" reliance "]})
    assert normalize_ticker(df)["ticker"][0] == "RELIANCE"