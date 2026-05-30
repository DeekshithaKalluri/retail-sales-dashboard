DROP VIEW IF EXISTS dim_customer;
DROP VIEW IF EXISTS dim_product;
DROP VIEW IF EXISTS dim_geography;
DROP VIEW IF EXISTS fact_orders;
DROP VIEW IF EXISTS kpi_summary;
DROP VIEW IF EXISTS kpi_monthly_trend;
DROP VIEW IF EXISTS kpi_regional;
DROP VIEW IF EXISTS kpi_category;
DROP VIEW IF EXISTS kpi_seasonality_gap;

CREATE VIEW dim_customer AS
SELECT DISTINCT customer_id, customer_name, segment
FROM read_csv_auto('output/superstore_clean.csv');

CREATE VIEW dim_product AS
SELECT DISTINCT product_id, product_name, category, sub_category
FROM read_csv_auto('output/superstore_clean.csv');

CREATE VIEW dim_geography AS
SELECT DISTINCT city, state, region, postal_code
FROM read_csv_auto('output/superstore_clean.csv');

CREATE VIEW fact_orders AS
SELECT
    order_id, order_date, ship_date, ship_mode, ship_days,
    customer_id, customer_name, segment,
    product_id, product_name, category, sub_category,
    city, state, region, postal_code,
    sales, quantity, discount, profit, profit_margin,
    order_year, order_month, order_quarter, month_name, season
FROM read_csv_auto('output/superstore_clean.csv');

CREATE VIEW kpi_summary AS
SELECT
    COUNT(DISTINCT order_id)           AS total_orders,
    ROUND(SUM(sales), 2)               AS total_revenue,
    ROUND(SUM(profit), 2)              AS total_profit,
    ROUND(AVG(profit_margin) * 100, 2) AS avg_profit_margin_pct,
    ROUND(AVG(ship_days), 1)           AS avg_ship_days
FROM fact_orders;

CREATE VIEW kpi_monthly_trend AS
SELECT
    order_year, order_month, month_name,
    ROUND(SUM(sales), 2)     AS monthly_revenue,
    ROUND(SUM(profit), 2)    AS monthly_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM fact_orders
GROUP BY order_year, order_month, month_name
ORDER BY order_year, order_month;

CREATE VIEW kpi_regional AS
SELECT
    region,
    ROUND(SUM(sales), 2)               AS region_revenue,
    ROUND(SUM(profit), 2)              AS region_profit,
    ROUND(AVG(profit_margin) * 100, 2) AS avg_margin_pct,
    COUNT(DISTINCT order_id)           AS order_count,
    COUNT(DISTINCT customer_id)        AS unique_customers
FROM fact_orders
GROUP BY region
ORDER BY region_revenue DESC;

CREATE VIEW kpi_category AS
SELECT
    category, sub_category,
    ROUND(SUM(sales), 2)               AS category_revenue,
    ROUND(SUM(profit), 2)              AS category_profit,
    ROUND(AVG(profit_margin) * 100, 2) AS avg_margin_pct,
    COUNT(DISTINCT order_id)           AS order_count
FROM fact_orders
GROUP BY category, sub_category
ORDER BY category_revenue DESC;

CREATE VIEW kpi_seasonality_gap AS
SELECT
    season,
    ROUND(SUM(sales), 2)               AS season_revenue,
    ROUND(AVG(sales), 2)               AS avg_order_value,
    COUNT(DISTINCT order_id)           AS order_count,
    ROUND(SUM(profit), 2)              AS season_profit,
    ROUND(AVG(profit_margin) * 100, 2) AS avg_margin_pct
FROM fact_orders
GROUP BY season
ORDER BY season_revenue DESC;