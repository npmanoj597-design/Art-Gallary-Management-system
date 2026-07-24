-- Converted to function `bookticket` returning the new ticket_id

DROP FUNCTION IF EXISTS bookticket(integer, integer, varchar);

CREATE OR REPLACE FUNCTION bookticket(
  p_visitor_id INTEGER,
  p_exhibition_id INTEGER,
  p_seat_type VARCHAR(50)
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
  v_price NUMERIC(12,2);
  v_ticket_id INTEGER;
BEGIN
  SELECT ticket_price
    INTO v_price
    FROM Exhibition
   WHERE exhibition_id = p_exhibition_id;

  IF v_price IS NULL THEN
    RAISE EXCEPTION 'bookticket: exhibition_id % not found', p_exhibition_id;
  END IF;

  INSERT INTO Ticket (visitor_id, exhibition_id, purchase_date, price, seat_type)
  VALUES (p_visitor_id, p_exhibition_id, CURRENT_DATE, v_price, p_seat_type)
  RETURNING ticket_id INTO v_ticket_id;

  RETURN v_ticket_id;
END;
$$;

