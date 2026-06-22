PRAGMA foreign_keys = ON;

CREATE TABLE companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    ticker TEXT UNIQUE,
    sector_id INTEGER
);

CREATE TABLE sectors (
    sector_id INTEGER PRIMARY KEY,
    sector_name TEXT NOT NULL
);

CREATE TABLE profitandloss (
    pnl_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    sales REAL,
    profit REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE balancesheet (
    bs_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    cf_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE analysis (
    analysis_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE documents (
    document_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    document_url TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE prosandcons (
    proscons_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    pros TEXT,
    cons TEXT,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    price_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    price_date DATE,
    close_price REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE financial_ratios (
    ratio_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roce REAL,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);

CREATE TABLE peer_groups (
    peer_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    peer_company_id INTEGER,
    FOREIGN KEY(company_id) REFERENCES companies(company_id)
);