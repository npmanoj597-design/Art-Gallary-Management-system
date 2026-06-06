-- Indexes for frequently queried columns (name, dates, emails)

CREATE INDEX IF NOT EXISTS idx_artist_name ON Artist (name);
CREATE INDEX IF NOT EXISTS idx_category_name ON Category (name);
CREATE INDEX IF NOT EXISTS idx_artwork_title ON Artwork (title);
CREATE INDEX IF NOT EXISTS idx_artwork_artist_id ON Artwork (artist_id);
CREATE INDEX IF NOT EXISTS idx_artwork_category_id ON Artwork (category_id);

CREATE INDEX IF NOT EXISTS idx_exhibition_start_end ON Exhibition (start_date, end_date);
CREATE INDEX IF NOT EXISTS idx_ticket_purchase_date ON Ticket (purchase_date);
CREATE INDEX IF NOT EXISTS idx_ticket_exhibition_id ON Ticket (exhibition_id);
CREATE INDEX IF NOT EXISTS idx_ticket_visitor_id ON Ticket (visitor_id);

CREATE INDEX IF NOT EXISTS idx_visitor_email ON Visitor (email);

CREATE INDEX IF NOT EXISTS idx_sale_sale_date ON Sale (sale_date);
CREATE INDEX IF NOT EXISTS idx_sale_artwork_id ON Sale (artwork_id);
CREATE INDEX IF NOT EXISTS idx_sale_visitor_id ON Sale (visitor_id);

-- Admin auth lookup
CREATE INDEX IF NOT EXISTS idx_admin_username ON AdminUser (username);

