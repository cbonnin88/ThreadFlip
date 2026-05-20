-- Identifies which apparel categories suffer from the worst checkout dropoffs 

WITH raw_funnel AS (

  SELECT
    session_id,
    event_type,
    REGEXP_EXTRACT(uri,r'/category/([^/?#]+)') AS extracted_category
  FROM `bigquery-public-data.thelook_ecommerce.events`
),
session_summary AS (

  SELECT
    session_id,
    MAX(extracted_category) AS category,
    MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS hit_cart,
    MAX(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS hit_purchase
  FROM raw_funnel
  WHERE extracted_category IS NOT NULL
  GROUP BY
    session_id
)
SELECT
  category,
  SUM(hit_cart) AS total_carts,
  SUM(hit_purchase) AS total_purchases,
  ROUND((1-(SUM(hit_purchase) / SUM(hit_cart))) * 100,2) AS category_cart_abandonment_rate
FROM session_summary
GROUP BY
  category
HAVING total_carts > 50
ORDER BY
  category_cart_abandonment_rate DESC;