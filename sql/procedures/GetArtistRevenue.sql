-- GetArtistRevenue stored procedure
-- Returns total revenue for an artist via OUT parameter

DROP PROCEDURE IF EXISTS GetArtistRevenue(integer, numeric);

CREATE OR REPLACE PROCEDURE GetArtistRevenue(
  IN p_artist_id INTEGER,
  OUT total_revenue NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
  SELECT COALESCE(SUM(s.amount_paid), 0)
    INTO total_revenue
  FROM Sale s
  JOIN Artwork a ON a.artwork_id = s.artwork_id
  WHERE a.artist_id = p_artist_id;
END;
$$;

