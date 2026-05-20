-- Measures how effectively inventory momves from list to sale across different product categories

SELECT 
  p.category,
  COUNT(DISTINCT p.id) AS total_product_cataloged,
  COUNT(DISTINCT oi.product_id) AS total_products_sold,
  ROUND((COUNT(DISTINCT oi.product_id) / COUNT(DISTINCT p.id)) * 100, 2) AS sell_through_rate
FROM `bigquery-public-data.thelook_ecommerce.products` AS p
LEFT JOIN `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  ON p.id = oi.product_id AND oi.status = 'Complete'
GROUP BY
  p.category
ORDER BY  
  sell_through_rate DESC;