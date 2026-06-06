-- Trigger: update Artwork.sold_count and log sales

CREATE OR REPLACE FUNCTION trg_update_artwork_sold_count()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- Increment count
  UPDATE Artwork
     SET sold_count = sold_count + 1
   WHERE artwork_id = NEW.artwork_id;

  -- Log sale (audit table)
  INSERT INTO ArtworkSaleLog (
    sale_id,
    artwork_id,
    visitor_id,
    sale_date,
    amount_paid,
    logged_at
  )
  VALUES (
    NEW.sale_id,
    NEW.artwork_id,
    NEW.visitor_id,
    NEW.sale_date,
    NEW.amount_paid,
    NOW()
  );

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS UpdateArtworkSoldCount ON Sale;

CREATE TRIGGER UpdateArtworkSoldCount
AFTER INSERT ON Sale
FOR EACH ROW
EXECUTE FUNCTION trg_update_artwork_sold_count();

