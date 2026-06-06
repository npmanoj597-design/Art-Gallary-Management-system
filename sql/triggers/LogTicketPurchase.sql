-- Trigger: auto-log ticket purchases

CREATE OR REPLACE FUNCTION trg_log_ticket_purchase()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO TicketPurchaseLog (
    ticket_id,
    visitor_id,
    exhibition_id,
    purchase_date,
    price,
    seat_type
  )
  VALUES (
    NEW.ticket_id,
    NEW.visitor_id,
    NEW.exhibition_id,
    NEW.purchase_date,
    NEW.price,
    NEW.seat_type
  );

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS LogTicketPurchase ON Ticket;

CREATE TRIGGER LogTicketPurchase
AFTER INSERT ON Ticket
FOR EACH ROW
EXECUTE FUNCTION trg_log_ticket_purchase();

