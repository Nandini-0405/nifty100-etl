import sqlite3
import pandas as pd


def get_connection():

    return sqlite3.connect(
        "db/nifty100.db"
    )


# ----------------------------------
# Test 1: financial_ratios exists
# ----------------------------------

def test_financial_ratios():

    conn = get_connection()

    df = pd.read_sql(

        """
        SELECT *
        FROM financial_ratios
        """,

        conn

    )

    assert len(df) > 0

    conn.close()


# ----------------------------------
# Test 2: peer_percentiles exists
# ----------------------------------

def test_peer_percentiles():

    conn = get_connection()

    df = pd.read_sql(

        """
        SELECT *
        FROM peer_percentiles
        """,

        conn

    )

    assert len(df) > 0

    conn.close()


# ----------------------------------
# Test 3: screener file exists
# ----------------------------------

def test_screener_output():

    import os

    assert os.path.exists(
        "output/screener_output.xlsx"
    )


# ----------------------------------
# Test 4: peer comparison exists
# ----------------------------------

def test_peer_output():

    import os

    assert os.path.exists(
        "output/peer_comparison.xlsx"
    )


# ----------------------------------
# Test 5: radar charts exist
# ----------------------------------

def test_radar_charts():

    import os

    assert os.path.exists(
        "reports/radar_charts"
    )