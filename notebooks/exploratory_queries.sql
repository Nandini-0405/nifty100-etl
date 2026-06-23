-- Q1 Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- Q2 Top 10 Companies by Market Cap
SELECT company_id,
       MAX(market_cap) AS max_market_cap
FROM market_cap
GROUP BY company_id
ORDER BY max_market_cap DESC
LIMIT 10;

-- Q3 Highest Revenue Companies
SELECT company_id,
       MAX(sales) AS highest_sales
FROM profitandloss
GROUP BY company_id
ORDER BY highest_sales DESC
LIMIT 10;

-- Q4 Highest Net Profit
SELECT company_id,
       MAX(net_profit) AS max_profit
FROM profitandloss
GROUP BY company_id
ORDER BY max_profit DESC
LIMIT 10;

-- Q5 Highest ROE
SELECT company_id,
       MAX(return_on_equity_pct) AS roe
FROM financial_ratios
GROUP BY company_id
ORDER BY roe DESC
LIMIT 10;

-- Q6 Sector Distribution
SELECT broad_sector,
       COUNT(*) AS companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC;

-- Q7 Companies With Highest Stock Price
SELECT company_id,
       MAX(close_price) AS highest_close
FROM stock_prices
GROUP BY company_id
ORDER BY highest_close DESC
LIMIT 10;

-- Q8 Average Dividend Yield
SELECT AVG(dividend_yield_pct)
AS avg_dividend_yield
FROM market_cap;

-- Q9 Companies With Most Years Data
SELECT company_id,
       COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
ORDER BY years DESC;

-- Q10 Average Net Profit Margin
SELECT AVG(net_profit_margin_pct)
AS avg_npm
FROM financial_ratios;