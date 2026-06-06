-- Trigger: enforce Sale.amount_paid matches Artwork.price

CREATE OR REPLACE FUNCTION trg_enforce_sale_amount_match()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
  v_artwork_price NUMERIC(12,2);
BEGIN
  SELECT price
    INTO v_artwork_price
    FROM Artwork
   WHERE artwork_id = NEW.artwork_id;

  IF v_artwork_price IS NULL THEN
    RAISE EXCEPTION 'Sale enforcement failed: artwork_id % not found', NEW.artwork_id;
  END IF;

  -- Compare with rounding to avoid numeric scale mismatch
  IF ROUND(NEW.amount_paid, 2) <> ROUND(v_artwork_price, 2) THEN
    RAISE EXCEPTION
      'Sale enforcement failed: amount_paid % must match Artwork.price % for artwork_id %',
      NEW.amount_paid, v_artwork_price, NEW.artwork_id;
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS EnforceSaleAmountMatchArtworkPrice ON Sale;

CREATE TRIGGER EnforceSaleAmountMatchArtworkPrice
BEFORE INSERT OR UPDATE ON Sale
FOR EACH ROW
EXECUTE FUNCTION trg_enforce_sale_amount_match();

