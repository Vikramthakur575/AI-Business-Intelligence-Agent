SQL_EXAMPLES = """
Example 1

Question:
Top 10 companies by revenue

SQL:
SELECT
symbol,
totalrevenue
FROM financials
ORDER BY totalrevenue DESC
LIMIT 10;

-----------------------

Example 2

Question:
Revenue trend for NVDA

SQL:
SELECT
fiscaldateending,
totalrevenue
FROM financials
WHERE symbol='NVDA'
ORDER BY fiscaldateending;

-----------------------

Example 3

Question:
Top EBITDA companies

SQL:
SELECT
symbol,
ebitda
FROM financials
ORDER BY ebitda DESC
LIMIT 10;

-----------------------

Example 4

Question:
Average revenue by company

SQL:
SELECT
symbol,
AVG(totalrevenue) AS avg_revenue
FROM financials
GROUP BY symbol
ORDER BY avg_revenue DESC;

-----------------------

Example 5

Question:
Top gross profit companies

SQL:
SELECT
symbol,
grossprofit
FROM financials
ORDER BY grossprofit DESC
LIMIT 10;

-----------------------

Only output SQL.
Never explain anything.
"""