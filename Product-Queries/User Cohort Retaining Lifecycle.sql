-- Tracks customer retention cohorts by seeing if users who signed up in a specific month continue to make purchases over subsequent months.

WITH
  user_cohorts AS (
    SELECT id AS user_id, TIMESTAMP_TRUNC(created_at, MONTH) AS cohort_month
    FROM `bigquery-public-data.thelook_ecommerce.users`
  ),
  user_orders AS (
    SELECT user_id, TIMESTAMP_TRUNC(created_at, MONTH) AS order_month,
    FROM `bigquery-public-data.thelook_ecommerce.orders`
    GROUP BY user_id, order_month
  )
SELECT
  c.cohort_month,
  COUNT(DISTINCT c.user_id) AS cohort_size,
  COUNT(
    DISTINCT
      CASE
        WHEN
          DATE(o.order_month)
          = DATE_ADD(DATE(c.cohort_month), INTERVAL 1 MONTH)
          THEN o.user_id
        END)
    AS month_1_retained,
  COUNT(
    DISTINCT
      CASE
        WHEN
          DATE(o.order_month)
          = DATE_ADD(DATE(c.cohort_month), INTERVAL 2 MONTH)
          THEN o.user_id
        END)
    AS month_2_retained
FROM user_cohorts AS c
LEFT JOIN user_orders AS o
  ON c.user_id = o.user_id
GROUP BY c.cohort_month
ORDER BY cohort_month DESC;
