-- Analyzing the concentration of marketplace value generation by charting running spend distributions

WITH user_spend AS (

  SELECT
    user_id,
    ROUND(SUM(sale_price),2) AS total_user_spend
  FROM `bigquery-public-data.thelook_ecommerce.order_items`
  WHERE status = 'Complete'
  GROUP BY
    user_id
)
SELECT
  user_id,
  user_spend.total_user_spend,
  ROUND(SUM(user_spend.total_user_spend) OVER(ORDER BY user_spend.total_user_spend DESC),2) AS running_cumulative_gmv
FROM user_spend
LIMIT 1000;