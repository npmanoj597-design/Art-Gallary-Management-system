DROP VIEW IF EXISTS ExhibitionSummary;

CREATE OR REPLACE VIEW ExhibitionSummary AS
SELECT
  e.exhibition_id,
  e.title,
  e.start_date,
  e.end_date,
  e.theme,
  c.name AS curator_name,
  COUNT(DISTINCT ae.artwork_id) AS artwork_count,
  COUNT(DISTINCT t.ticket_id) AS ticket_count,
  COALESCE(SUM(t.price), 0) AS total_ticket_revenue
FROM Exhibition e
LEFT JOIN Curator c ON c.curator_id = e.curator_id
LEFT JOIN Artwork_Exhibition ae ON ae.exhibition_id = e.exhibition_id
LEFT JOIN Ticket t ON t.exhibition_id = e.exhibition_id
GROUP BY
  e.exhibition_id, e.title, e.start_date, e.end_date, e.theme, c.name;

