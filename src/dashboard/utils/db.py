import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "db/nifty100.db"


@st.cache_data(ttl=600)
def get_companies():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM companies
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):

    conn = sqlite3.connect(DB_PATH)

    query = f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id = '{ticker}'
    """

    if year:

        query += f" AND year = '{year}'"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


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