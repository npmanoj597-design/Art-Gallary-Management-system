-- Converted to function `getartistrevenue` to return numeric total revenue

DROP FUNCTION IF EXISTS getartistrevenue(integer);

CREATE OR REPLACE FUNCTION getartistrevenue(
  p_artist_id INTEGER
) RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
  total_revenue NUMERIC;
BEGIN
  SELECT COALESCE(SUM(s.amount_paid), 0)
    INTO total_revenue
  FROM Sale s
  JOIN Artwork a ON a.artwork_id = s.artwork_id
  WHERE a.artist_id = p_artist_id;

  RETURN total_revenue;
END;
$$;

