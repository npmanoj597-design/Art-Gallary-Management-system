DROP VIEW IF EXISTS ArtworkSalesReport;

CREATE OR REPLACE VIEW ArtworkSalesReport AS
SELECT
  a.artwork_id,
  a.title,
  ar.name AS artist_name,
  cat.name AS category_name,
  COUNT(s.sale_id) AS sale_count,
  COALESCE(SUM(s.amount_paid), 0) AS total_revenue
FROM Artwork a
INNER JOIN Artist ar ON ar.artist_id = a.artist_id
INNER JOIN Category cat ON cat.category_id = a.category_id
INNER JOIN Sale s ON s.artwork_id = a.artwork_id
GROUP BY
  a.artwork_id, a.title, ar.name, cat.name
HAVING COUNT(s.sale_id) >= 1;

