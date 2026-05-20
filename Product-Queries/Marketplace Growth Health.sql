-- Tracks the monthly gorss merchandise value (GMV) and total orders to understand the marketplace baseline trajectory

SELECT
  TIMESTAMP_TRUNC(created_at, MONTH) AS order_month,
  COUNT(DISTINCT order_id) AS total_orders,
  ROUND(SUM(sale_price),2) AS gross_merchandise_value_gmv,
  COUNT(DISTINCT user_id) AS unique_active_buyers  
FROM `bigquery-public-data.thelook_ecommerce.order_items`
WHERE status NOT IN ('Cancelled','Returned')
GROUP BY
  order_month
ORDER BY
  order_month DESC;