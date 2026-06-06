-- Sample data for the Art Gallery Management System
-- Assumes triggers are created before seeding (so sold_count and log tables populate).

-- Enable pgcrypto for seeded bcrypt hashes (admin login)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ----------------------------
-- Curators (>= 10 rows)
-- ----------------------------
INSERT INTO Curator (curator_id, name, email, phone) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Meera Iyer', 'meera.iyer@museum.example', '+91-9000011111'),
  (2, 'Louis Bernard', 'louis.bernard@museum.example', '+33-6000022222'),
  (3, 'Aya Tanaka', 'aya.tanaka@museum.example', '+81-7000033333'),
  (4, 'Claire Morgan', 'claire.morgan@museum.example', '+44-8000044444'),
  (5, 'Ravi Shankar', 'ravi.shankar@museum.example', '+91-9000055555'),
  (6, 'Sophie Martin', 'sophie.martin@museum.example', '+33-6000066666'),
  (7, 'Marco Rossi', 'marco.rossi@museum.example', '+39-7000077777'),
  (8, 'Amrita Sen', 'amrita.sen@museum.example', '+91-9000088888'),
  (9, 'Noah Williams', 'noah.williams@museum.example', '+1-8000099999'),
  (10, 'Priya Nair', 'priya.nair@museum.example', '+91-9000101010');

-- ----------------------------
-- Categories (5 rows as required)
-- ----------------------------
INSERT INTO Category (category_id, name, description) OVERRIDING SYSTEM VALUE VALUES
  (1, 'painting', 'Painted works on canvas and board'),
  (2, 'sculpture', '3D works in stone, metal, and mixed media'),
  (3, 'photography', 'Captures and archival prints'),
  (4, 'digital', 'Digitally generated and interactive pieces'),
  (5, 'print', 'Reproductions and limited edition prints');

-- ----------------------------
-- Artists (10 rows as required)
-- ----------------------------
INSERT INTO Artist (artist_id, name, nationality, birth_year, bio) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Rahul Mehta', 'India', 1982, 'Modern compositions with layered color fields.'),
  (2, 'Anita Kapoor', 'India', 1976, 'Narrative painting inspired by folklore and city life.'),
  (3, 'Sofia Alvarez', 'Spain', 1985, 'Light-driven studies in sculpture and form.'),
  (4, 'Kenji Sato', 'Japan', 1979, 'Minimal photography with long exposure textures.'),
  (5, 'Amelie Durand', 'France', 1988, 'Digital works exploring memory and motion.'),
  (6, 'William Carter', 'United States', 1973, 'Printmaking focused on geometry and rhythm.'),
  (7, 'Aisha Rahman', 'India', 1990, 'Sculptures in bronze and recycled materials.'),
  (8, 'Lucia Romano', 'Italy', 1981, 'Painting with mythic undertones and bold strokes.'),
  (9, 'Noor Hassan', 'UAE', 1984, 'Photography documenting coastal life and light.'),
  (10, 'Emma Clarke', 'United Kingdom', 1977, 'Mixed medium prints with contemporary symbolism.');

-- ----------------------------
-- Exhibitions (4 rows as required; 2 ongoing, 2 past)
-- ----------------------------
INSERT INTO Exhibition (exhibition_id, title, start_date, end_date, theme, curator_id, ticket_price) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Modern Visions', '2026-01-10', '2026-12-10', 'Color, memory, and motion', 1, 120.00),
  (2, 'Heritage in Light', '2026-03-01', '2026-09-30', 'Light studies and archival echoes', 2, 80.00),
  (3, 'Sculpting the Future', '2025-02-01', '2025-06-30', 'Form in steel and silence', 3, 100.00),
  (4, 'Prints & Memories', '2024-08-01', '2024-11-30', 'Limited editions and personal archives', 4, 60.00);

-- ----------------------------
-- Artworks (25 rows)
-- Distribute across 5 categories
-- ----------------------------
INSERT INTO Artwork (artwork_id, title, year_created, medium, price, sold_count, artist_id, category_id) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Skyfold No.1', 2023, 'Acrylic on canvas', 3500.00, 0, 1, 1),
  (2, 'Kite Strings', 2024, 'Acrylic on board', 2200.00, 0, 2, 1),
  (3, 'Urban Folklore', 2022, 'Mixed media on canvas', 4100.00, 0, 2, 1),
  (4, 'Afterimage Study', 2021, 'Oil on canvas', 2800.00, 0, 8, 1),
  (5, 'Mythic Tide', 2020, 'Gouache on paper', 1900.00, 0, 8, 1),

  (6, 'Bronze Lattice', 2023, 'Bronze sculpture', 9500.00, 0, 7, 2),
  (7, 'Recycled Geometry', 2022, 'Steel and recycled fragments', 7200.00, 0, 7, 2),
  (8, 'Silent Balance', 2024, 'Stone and resin', 6800.00, 0, 3, 2),
  (9, 'Lumen Column', 2021, 'Aluminum and glass', 7600.00, 0, 3, 2),
  (10, 'Edge of Form', 2020, 'Mixed metal', 5400.00, 0, 7, 2),

  (11, 'Long Exposure Rain', 2024, 'Archival pigment print', 2600.00, 0, 4, 3),
  (12, 'Night Market Light', 2023, 'Archival pigment print', 3000.00, 0, 4, 3),
  (13, 'Coastal Frames', 2022, 'Archival pigment print', 2400.00, 0, 9, 3),
  (14, 'Blue Hour Study', 2021, 'Archival pigment print', 2150.00, 0, 9, 3),
  (15, 'Monsoon Lines', 2020, 'Archival pigment print', 1950.00, 0, 4, 3),

  (16, 'Memory Drift', 2025, 'Generative digital artwork', 4800.00, 0, 5, 4),
  (17, 'Motion Relics', 2024, 'Interactive digital installation', 6200.00, 0, 5, 4),
  (18, 'Spectral Bloom', 2023, 'Digital collage', 3900.00, 0, 5, 4),
  (19, 'Signal Garden', 2022, 'Generative digital artwork', 4100.00, 0, 5, 4),
  (20, 'Echo Engine', 2021, 'Procedural graphics', 3500.00, 0, 5, 4),

  (21, 'Geometric Verse', 2023, 'Limited edition screen print', 1600.00, 0, 6, 5),
  (22, 'Rhythm & Grid', 2024, 'Limited edition lithograph', 2100.00, 0, 6, 5),
  (23, 'Symbolic Margin', 2022, 'Printmaking series', 1800.00, 0, 10, 5),
  (24, 'Archive Bloom', 2021, 'Limited edition etching', 2500.00, 0, 10, 5),
  (25, 'Quiet Motif', 2020, 'Limited edition lithograph', 1700.00, 0, 6, 5);

-- ----------------------------
-- Artwork <-> Exhibition mapping (many-to-many)
-- ----------------------------
-- Modern Visions (1): artworks 1-12, plus 16,21
INSERT INTO Artwork_Exhibition (artwork_id, exhibition_id) OVERRIDING SYSTEM VALUE VALUES
  (1, 1), (2, 1), (3, 1), (4, 1), (5, 1),
  (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
  (11, 1), (12, 1),
  (16, 1), (21, 1);

-- Heritage in Light (2): artworks 4,5,11-15,18-20,22
INSERT INTO Artwork_Exhibition (artwork_id, exhibition_id) OVERRIDING SYSTEM VALUE VALUES
  (4, 2), (5, 2),
  (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
  (18, 2), (19, 2), (20, 2),
  (22, 2);

-- Sculpting the Future (3): artworks 6-10,8,13,17,23
INSERT INTO Artwork_Exhibition (artwork_id, exhibition_id) OVERRIDING SYSTEM VALUE VALUES
  (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
  (13, 3),
  (17, 3),
  (23, 3);

-- Prints & Memories (4): artworks 15,19,21-25,23-24
INSERT INTO Artwork_Exhibition (artwork_id, exhibition_id) OVERRIDING SYSTEM VALUE VALUES
  (15, 4),
  (19, 4),
  (21, 4), (22, 4), (23, 4), (24, 4), (25, 4);

-- ----------------------------
-- Visitors (20 rows as required)
-- ----------------------------
INSERT INTO Visitor (visitor_id, name, email, phone, membership_type) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Aarav Singh', 'aarav.singh@example.com', '+91-8000001001', 'Regular'),
  (2, 'Mehnaz Khan', 'mehnaz.khan@example.com', '+91-8000001002', 'Premium'),
  (3, 'Hugo Martin', 'hugo.martin@example.com', '+33-7000001003', 'Regular'),
  (4, 'Mina Cho', 'mina.cho@example.com', '+82-7000001004', 'Student'),
  (5, 'Oliver Brooks', 'oliver.brooks@example.com', '+44-7000001005', 'Regular'),
  (6, 'Priyanka Das', 'priyanka.das@example.com', '+91-8000001006', 'Student'),
  (7, 'Sophia Weber', 'sophia.weber@example.com', '+49-7000001007', 'Premium'),
  (8, 'Zaid Rahman', 'zaid.rahman@example.com', '+971-7000001008', 'Regular'),
  (9, 'Clara Johnson', 'clara.johnson@example.com', '+1-7000001009', 'Premium'),
  (10, 'Santiago Ruiz', 'santiago.ruiz@example.com', '+34-7000001010', 'Regular'),
  (11, 'Neha Verma', 'neha.verma@example.com', '+91-8000001011', 'Regular'),
  (12, 'Lucas Silva', 'lucas.silva@example.com', '+55-7000001012', 'Student'),
  (13, 'Farah Saleh', 'farah.saleh@example.com', '+971-7000001013', 'Premium'),
  (14, 'Ben Carter', 'ben.carter@example.com', '+1-7000001014', 'Regular'),
  (15, 'Yuki Nakamura', 'yuki.nakamura@example.com', '+81-7000001015', 'Student'),
  (16, 'Evelyn Ward', 'evelyn.ward@example.com', '+1-7000001016', 'Premium'),
  (17, 'Arjun Pillai', 'arjun.pillai@example.com', '+91-8000001017', 'Regular'),
  (18, 'Grace Thompson', 'grace.thompson@example.com', '+1-7000001018', 'Student'),
  (19, 'Mateo Garcia', 'mateo.garcia@example.com', '+34-7000001019', 'Regular'),
  (20, 'Zara Ali', 'zara.ali@example.com', '+971-7000001020', 'Premium');

-- ----------------------------
-- Tickets (20 rows; one per visitor)
-- purchase_date must be DATE; keep within exhibition dates
-- ----------------------------
INSERT INTO Ticket (ticket_id, visitor_id, exhibition_id, purchase_date, price, seat_type) OVERRIDING SYSTEM VALUE VALUES
  (1, 1, 1, '2026-02-02', 120.00, 'A1'),
  (2, 2, 1, '2026-02-10', 120.00, 'A2'),
  (3, 3, 2, '2026-04-12', 80.00, 'B1'),
  (4, 4, 2, '2026-05-01', 80.00, 'B2'),
  (5, 5, 1, '2026-03-18', 120.00, 'C1'),
  (6, 6, 2, '2026-06-06', 80.00, 'D1'),
  (7, 7, 1, '2026-07-07', 120.00, 'A3'),
  (8, 8, 1, '2026-08-08', 120.00, 'A4'),
  (9, 9, 2, '2026-03-25', 80.00, 'B3'),
  (10, 10, 2, '2026-04-28', 80.00, 'B4'),
  (11, 11, 1, '2026-05-15', 120.00, 'C2'),
  (12, 12, 2, '2026-06-20', 80.00, 'D2'),
  (13, 13, 1, '2026-09-01', 120.00, 'A5'),
  (14, 14, 2, '2026-07-19', 80.00, 'C3'),
  (15, 15, 1, '2026-01-20', 120.00, 'E1'),
  (16, 16, 1, '2026-02-25', 120.00, 'E2'),
  (17, 17, 2, '2026-08-21', 80.00, 'F1'),
  (18, 18, 1, '2026-09-10', 120.00, 'F2'),
  (19, 19, 2, '2026-04-03', 80.00, 'G1'),
  (20, 20, 1, '2026-05-30', 120.00, 'G2');

-- ----------------------------
-- Sales (8 rows as required)
-- amount_paid must match Artwork.price (enforced by trigger)
-- ----------------------------
INSERT INTO Sale (sale_id, artwork_id, visitor_id, sale_date, amount_paid) OVERRIDING SYSTEM VALUE VALUES
  (1, 1, 1, '2026-02-15', 3500.00),
  (2, 6, 2, '2026-03-02', 9500.00),
  (3, 11, 3, '2026-04-20', 2600.00),
  (4, 16, 4, '2026-06-15', 4800.00),
  (5, 21, 5, '2026-03-25', 1600.00),
  (6, 7, 7, '2026-07-08', 7200.00),
  (7, 23, 9, '2026-08-10', 1800.00),
  (8, 13, 14, '2026-05-18', 2400.00);

-- ----------------------------
-- Staff (10 rows)
-- ----------------------------
INSERT INTO Staff (staff_id, name, role, email, salary) OVERRIDING SYSTEM VALUE VALUES
  (1, 'Arnav Sharma', 'Curatorial Assistant', 'arnav.sharma@museum.example', 42000.00),
  (2, 'Fatima Noor', 'Gallery Technician', 'fatima.noor@museum.example', 38000.00),
  (3, 'Ethan Wright', 'Security Officer', 'ethan.wright@museum.example', 45000.00),
  (4, 'Kavya Iyer', 'Marketing Manager', 'kavya.iyer@museum.example', 62000.00),
  (5, 'Matteo Bianchi', 'Collections Manager', 'matteo.bianchi@museum.example', 70000.00),
  (6, 'Sara Costa', 'Education Coordinator', 'sara.costa@museum.example', 41000.00),
  (7, 'Priyansh Rao', 'IT Support', 'priyansh.rao@museum.example', 36000.00),
  (8, 'Hannah Lee', 'Front Desk', 'hannah.lee@museum.example', 30000.00),
  (9, 'Imran Qureshi', 'Facilities', 'imran.qureshi@museum.example', 33000.00),
  (10, 'Charlotte King', 'Finance Officer', 'charlotte.king@museum.example', 56000.00);

-- ----------------------------
-- Seed admin user (username: admin / password: admin123)
-- ----------------------------
INSERT INTO AdminUser (admin_id, username, password_hash, role, created_at) OVERRIDING SYSTEM VALUE VALUES
  (
    1,
    'admin',
    crypt('admin123', gen_salt('bf')),
    'admin',
    NOW()
  );

-- ----------------------------
-- Demonstrate UPDATE + DELETE + cascades + transaction rollback
-- ----------------------------
-- UPDATE example: adjust a description via medium field (kept consistent with artwork)
UPDATE Artwork
SET medium = 'Acrylic on canvas (restored)'
WHERE artwork_id = 1;

-- DELETE + cascades example with rollback: delete a visitor and rollback
BEGIN;
  DELETE FROM Visitor WHERE visitor_id = 20;
ROLLBACK;

