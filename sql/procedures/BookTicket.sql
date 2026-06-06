-- BookTicket stored procedure
-- Creates a Ticket within the caller's transaction.
-- Uses Exhibition.ticket_price so the client does not need to provide price.

DROP PROCEDURE IF EXISTS BookTicket(integer, integer, varchar, integer);

CREATE OR REPLACE PROCEDURE BookTicket(
  IN p_visitor_id INTEGER,
  IN p_exhibition_id INTEGER,
  IN p_seat_type VARCHAR(50),
  INOUT p_ticket_id INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_price NUMERIC(12,2);
BEGIN
  SELECT ticket_price
    INTO v_price
    FROM Exhibition
   WHERE exhibition_id = p_exhibition_id;

  IF v_price IS NULL THEN
    RAISE EXCEPTION 'BookTicket: exhibition_id % not found', p_exhibition_id;
  END IF;

  INSERT INTO Ticket (visitor_id, exhibition_id, purchase_date, price, seat_type)
  VALUES (p_visitor_id, p_exhibition_id, CURRENT_DATE, v_price, p_seat_type)
  RETURNING ticket_id INTO p_ticket_id;
END;
$$;

