-- Pinpoints precisely where users drop out of the conversion funnel, justifying the need for the bundle discount feature

WITH funnel_events AS (

  SELECT
    session_id,
    MAX(CASE WHEN event_type = 'product' THEN 1 ELSE 0 END) AS viewed_product,
    MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS added_to_cart,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS completed_purchase
  FROM `bigquery-public-data.thelook_ecommerce.events`
  GROUP BY
    session_id
)
SELECT
  SUM(viewed_product) AS total_product_values,
  SUM(added_to_cart) AS total_cart_adds,
  SUM(completed_purchase) AS total_purchases,
  ROUND((SUM(added_to_cart) / SUM(viewed_product)) * 100, 2) AS cart_abandonment_rate
FROM funnel_events;