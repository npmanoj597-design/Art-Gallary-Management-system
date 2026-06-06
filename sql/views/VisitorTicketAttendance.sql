DROP VIEW IF EXISTS VisitorTicketAttendance;

-- Uses RIGHT JOIN + LEFT JOIN to satisfy JOIN type requirement
CREATE OR REPLACE VIEW VisitorTicketAttendance AS
SELECT
  v.visitor_id,
  v.name AS visitor_name,
  v.email,
  v.membership_type,
  COUNT(t.ticket_id) AS tickets_purchased,
  COALESCE(SUM(t.price), 0) AS total_spent,
  MAX(e.end_date) AS latest_exhibition_end_date
FROM Ticket t
RIGHT JOIN Visitor v ON v.visitor_id = t.visitor_id
LEFT JOIN Exhibition e ON e.exhibition_id = t.exhibition_id
GROUP BY
  v.visitor_id, v.name, v.email, v.membership_type;

