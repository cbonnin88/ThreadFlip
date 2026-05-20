-- Pinpoints the top 5% of users generating inventory value to help us build tools for our power supply side

SELECT
  user_id,
  total_sales_volume,
  items_sold
FROM (
  SELECT
    user_id,
    SUM(sale_price) AS total_sales_volume,
    COUNT(id) AS items_sold,
    NTILE(20) OVER(ORDER BY SUM(sale_price) DESC) AS sales_tier
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE status = 'Complete'
  GROUP BY
    user_id
)
WHERE sales_tier = 1
ORDER BY
  total_sales_volume DESC;