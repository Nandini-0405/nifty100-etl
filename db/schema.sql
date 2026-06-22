PRAGMA foreign_keys = ON;

CREATE TABLE sectors (
    sector_id TEXT PRIMARY KEY,
    sector_name TEXT
);

CREATE TABLE companies (
    company_id TEXT PRIMARY KEY,
    company_name TEXT,
    sector_id TEXT,
    website TEXT,

    FOREIGN KEY (sector_id)
    REFERENCES sectors(sector_id)
);

CREATE TABLE profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    net_profit REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE balancesheet (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE cashflow (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE analysis (
    id INTEGER PRIMARY KEY,
    company_id TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    document_url TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE prosandcons (
    id INTEGER PRIMARY KEY,
    company_id TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    date TEXT,
    open_price REAL,
    high_price REAL,
    low_price REAL,
    close_price REAL,
    volume REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE financial_ratios (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    year TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);

CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    company_id TEXT,
    peer_company_id TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(company_id)
);