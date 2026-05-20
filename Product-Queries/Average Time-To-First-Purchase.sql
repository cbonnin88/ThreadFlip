-- Calculates the latency between user acquisitioin and their first activatioin transaction event.

WITH ordered_purchases AS (

  SELECT
    user_id,
    created_at AS purchase_time,
    ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at ASC) AS purchase_sequence
  FROM `bigquery-public-data.thelook_ecommerce.orders`
)
SELECT
  ROUND(AVG(TIMESTAMP_DIFF(op.purchase_time, u.created_at,DAY)),1) AS avg_days_to_activate
FROM `bigquery-public-data.thelook_ecommerce.users` AS u
INNER JOIN ordered_purchases AS op
  ON u.id = op.user_id
WHERE op.purchase_sequence = 1;