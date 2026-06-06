DROP VIEW IF EXISTS ArtistSalesStats;

-- Covers AVG, MAX, MIN with GROUP BY + HAVING across 3+ tables
CREATE OR REPLACE VIEW ArtistSalesStats AS
SELECT
  ar.artist_id,
  ar.name AS artist_name,
  COUNT(s.sale_id) AS sale_count,
  SUM(s.amount_paid) AS total_revenue,
  AVG(s.amount_paid) AS avg_sale_amount,
  MAX(s.amount_paid) AS max_sale_amount,
  MIN(s.amount_paid) AS min_sale_amount
FROM Artist ar
INNER JOIN Artwork aw ON aw.artist_id = ar.artist_id
INNER JOIN Sale s ON s.artwork_id = aw.artwork_id
GROUP BY ar.artist_id, ar.name
HAVING COUNT(s.sale_id) >= 1;

