import os
import sqlite3


DB_PATH = "db/nifty100.db"


def test_database_exists():

    assert os.path.exists(DB_PATH)


def test_financial_ratios_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='financial_ratios'
        """
    )

    result = cursor.fetchone()

    conn.close()

    assert result is not None


def test_peer_percentiles_table():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='peer_percentiles'
        """
    )

    result = cursor.fetchone()

    conn.close()

    assert result is not None


def test_output_files():

    files = [

        "output/screener_output.xlsx",

        "output/peer_comparison.xlsx",

        "output/valuation_summary.xlsx",

        "output/valuation_flags.csv",

    ]

    for file in files:

        assert os.path.exists(file)


def test_radar_chart_folder():

    assert os.path.exists(

        "reports/radar_charts"

    )