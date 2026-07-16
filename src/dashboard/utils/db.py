import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


# -----------------------------------
# Companies
# -----------------------------------

@st.cache_data(ttl=600)
def get_companies():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Financial Ratios
# -----------------------------------

@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id = '{ticker}'
    """

    if year is not None:

        query += f" AND year = '{year}'"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------
# Profit & Loss
# -----------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        f"""
        SELECT *
        FROM profitandloss
        WHERE company_id = '{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Balance Sheet
# -----------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        f"""
        SELECT *
        FROM balancesheet
        WHERE company_id = '{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Cash Flow
# -----------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        f"""
        SELECT *
        FROM cashflow
        WHERE company_id = '{ticker}'
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Sectors
# -----------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM sectors
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Peer Groups
# -----------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        f"""
        SELECT *
        FROM peer_groups
        WHERE peer_group_name = '{group_name}'
        """,
        conn
    )

    conn.close()

    return df


# -----------------------------------
# Valuation
# -----------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = sqlite3.connect(DB_PATH)

    try:

        df = pd.read_sql(
            f"""
            SELECT *
            FROM valuation
            WHERE company_id = '{ticker}'
            """,
            conn
        )

    except:

        df = pd.DataFrame()

    conn.close()

    return df


# -----------------------------------
# Dashboard Data
# -----------------------------------

@st.cache_data(ttl=600)
def get_dashboard_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fr.*,
        s.broad_sector
    FROM financial_ratios fr
    LEFT JOIN sectors s
    ON fr.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------
# Screener Data
# -----------------------------------

@st.cache_data(ttl=600)
def get_screener_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fr.*,
        c.company_name,
        s.broad_sector
    FROM financial_ratios fr

    LEFT JOIN companies c
    ON fr.company_id = c.id

    LEFT JOIN sectors s
    ON fr.company_id = s.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# -----------------------------------
# Peer Data
# -----------------------------------

@st.cache_data(ttl=600)
def get_peer_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        """,
        conn
    )

    conn.close()

    return df