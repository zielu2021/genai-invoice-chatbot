import sqlite3
import os

# Remove existing database for fresh start
if os.path.exists("invoices.db"):
    os.remove("invoices.db")

conn = sqlite3.connect("invoices.db")
cursor = conn.cursor()

cursor.executescript("""
-- =====================
-- CUSTOMERS TABLE
-- =====================
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    nip TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    country TEXT DEFAULT 'Poland',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- =====================
-- SERVICE CATEGORIES TABLE (NEW)
-- =====================
CREATE TABLE IF NOT EXISTS service_categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- =====================
-- INVOICES TABLE (ENHANCED)
-- =====================
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL UNIQUE,
    customer_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    status TEXT CHECK(status IN ('paid', 'unpaid', 'overdue', 'draft', 'cancelled')),
    payment_date TEXT,
    payment_method TEXT,
    notes TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- =====================
-- INVOICE ITEMS TABLE (ENHANCED)
-- =====================
CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    description TEXT,
    category_id INTEGER,
    quantity REAL,
    unit_price REAL,
    vat_rate REAL DEFAULT 0.23,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (category_id) REFERENCES service_categories(id)
);

-- =====================
-- PAYMENTS TABLE (NEW)
-- =====================
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    amount REAL NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT CHECK(payment_method IN ('bank_transfer', 'credit_card', 'cash', 'paypal')),
    reference TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);

-- =====================
-- RECURRING INVOICES TABLE (NEW)
-- =====================
CREATE TABLE IF NOT EXISTS recurring_templates (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    description TEXT,
    amount REAL,
    frequency TEXT CHECK(frequency IN ('monthly', 'quarterly', 'yearly')),
    next_invoice_date TEXT,
    is_active INTEGER DEFAULT 1,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- =====================
-- INSERT SERVICE CATEGORIES
-- =====================
INSERT INTO service_categories VALUES (1, 'Development', 'Software development and programming services');
INSERT INTO service_categories VALUES (2, 'Consulting', 'IT consulting and advisory services');
INSERT INTO service_categories VALUES (3, 'Training', 'Technical training and workshops');
INSERT INTO service_categories VALUES (4, 'Data Services', 'Data analysis, engineering, and ML');
INSERT INTO service_categories VALUES (5, 'Design', 'UI/UX and graphic design');
INSERT INTO service_categories VALUES (6, 'Support', 'Technical support and maintenance');
INSERT INTO service_categories VALUES (7, 'Infrastructure', 'Cloud and infrastructure services');

-- =====================
-- INSERT CUSTOMERS (EXPANDED FROM 5 TO 12)
-- =====================
INSERT INTO customers VALUES (1, 'ABC Solutions Ltd.', '1234567890', 'abc@solutions.com', '+48 22 123 4567', 'Warsaw', 'Poland', '2023-06-15');
INSERT INTO customers VALUES (2, 'XYZ Tech', '0987654321', 'xyz@tech.com', '+48 12 987 6543', 'Krakow', 'Poland', '2023-08-20');
INSERT INTO customers VALUES (3, 'John Smith Consulting', '1122334455', 'john@smith.com', '+48 58 111 2233', 'Gdansk', 'Poland', '2023-09-10');
INSERT INTO customers VALUES (4, 'DataFlow GmbH', '9876543210', 'contact@dataflow.de', '+49 30 456 7890', 'Berlin', 'Germany', '2023-11-05');
INSERT INTO customers VALUES (5, 'Nordic Analytics', '5544332211', 'hello@nordic.se', '+46 8 765 4321', 'Stockholm', 'Sweden', '2024-01-12');
INSERT INTO customers VALUES (6, 'TechVenture Capital', '6677889900', 'invest@techventure.com', '+48 22 555 6677', 'Warsaw', 'Poland', '2024-02-18');
INSERT INTO customers VALUES (7, 'CloudFirst Systems', '7788990011', 'hello@cloudfirst.io', '+48 71 888 9900', 'Wroclaw', 'Poland', '2024-03-22');
INSERT INTO customers VALUES (8, 'FinTech Innovations', '8899001122', 'contact@fintechinno.com', '+48 61 777 8899', 'Poznan', 'Poland', '2024-04-15');
INSERT INTO customers VALUES (9, 'E-Commerce Pro', '9900112233', 'orders@ecompro.pl', '+48 32 666 7788', 'Katowice', 'Poland', '2024-05-08');
INSERT INTO customers VALUES (10, 'HealthTech Solutions', '0011223344', 'info@healthtech.pl', '+48 42 555 6677', 'Lodz', 'Poland', '2024-06-20');
INSERT INTO customers VALUES (11, 'MediaWorks Agency', '1122334456', 'projects@mediaworks.pl', '+48 91 444 5566', 'Szczecin', 'Poland', '2024-07-14');
INSERT INTO customers VALUES (12, 'StartupHub Accelerator', '2233445567', 'partners@startuphub.eu', '+48 85 333 4455', 'Bialystok', 'Poland', '2024-08-01');

-- =====================
-- INSERT INVOICES (EXPANDED FROM 15 TO 35)
-- =====================
-- 2024 Invoices
INSERT INTO invoices VALUES (1,  'INV/2024/001', 1, '2024-01-15', '2024-02-15', 'paid', '2024-02-10', 'bank_transfer', 'Initial project setup');
INSERT INTO invoices VALUES (2,  'INV/2024/002', 2, '2024-02-10', '2024-03-10', 'paid', '2024-03-05', 'bank_transfer', NULL);
INSERT INTO invoices VALUES (3,  'INV/2024/003', 1, '2024-03-05', '2024-04-05', 'paid', '2024-04-01', 'bank_transfer', 'Phase 2 delivery');
INSERT INTO invoices VALUES (4,  'INV/2024/004', 3, '2024-03-20', '2024-04-20', 'overdue', NULL, NULL, 'Awaiting client response');
INSERT INTO invoices VALUES (5,  'INV/2024/005', 2, '2024-04-01', '2024-05-01', 'paid', '2024-04-28', 'credit_card', NULL);
INSERT INTO invoices VALUES (6,  'INV/2024/006', 4, '2024-05-10', '2024-06-10', 'paid', '2024-06-08', 'bank_transfer', 'German client - EUR');
INSERT INTO invoices VALUES (7,  'INV/2024/007', 5, '2024-06-15', '2024-07-15', 'paid', '2024-07-12', 'bank_transfer', 'Nordic expansion project');
INSERT INTO invoices VALUES (8,  'INV/2024/008', 1, '2024-07-01', '2024-08-01', 'unpaid', NULL, NULL, 'Follow-up sent');
INSERT INTO invoices VALUES (9,  'INV/2024/009', 3, '2024-08-20', '2024-09-20', 'unpaid', NULL, NULL, NULL);
INSERT INTO invoices VALUES (10, 'INV/2024/010', 4, '2024-09-05', '2024-10-05', 'paid', '2024-10-02', 'bank_transfer', NULL);
INSERT INTO invoices VALUES (11, 'INV/2024/011', 2, '2024-10-12', '2024-11-12', 'paid', '2024-11-10', 'bank_transfer', NULL);
INSERT INTO invoices VALUES (12, 'INV/2024/012', 5, '2024-11-01', '2024-12-01', 'overdue', NULL, NULL, 'Second reminder sent');
INSERT INTO invoices VALUES (13, 'INV/2024/013', 6, '2024-06-01', '2024-07-01', 'paid', '2024-06-28', 'bank_transfer', 'VC client onboarding');
INSERT INTO invoices VALUES (14, 'INV/2024/014', 7, '2024-07-15', '2024-08-15', 'paid', '2024-08-12', 'bank_transfer', 'Cloud migration project');
INSERT INTO invoices VALUES (15, 'INV/2024/015', 8, '2024-08-01', '2024-09-01', 'paid', '2024-08-29', 'credit_card', 'FinTech API development');
INSERT INTO invoices VALUES (16, 'INV/2024/016', 9, '2024-09-10', '2024-10-10', 'paid', '2024-10-08', 'bank_transfer', 'E-commerce platform');
INSERT INTO invoices VALUES (17, 'INV/2024/017', 10, '2024-10-01', '2024-11-01', 'paid', '2024-10-30', 'bank_transfer', 'Healthcare app MVP');
INSERT INTO invoices VALUES (18, 'INV/2024/018', 11, '2024-10-20', '2024-11-20', 'paid', '2024-11-18', 'paypal', 'Website redesign');
INSERT INTO invoices VALUES (19, 'INV/2024/019', 12, '2024-11-05', '2024-12-05', 'unpaid', NULL, NULL, 'Startup accelerator program');
INSERT INTO invoices VALUES (20, 'INV/2024/020', 6, '2024-11-15', '2024-12-15', 'paid', '2024-12-10', 'bank_transfer', NULL);

-- 2025 Invoices
INSERT INTO invoices VALUES (21, 'INV/2025/001', 1, '2025-01-10', '2025-02-10', 'paid', '2025-02-08', 'bank_transfer', 'Annual contract renewal');
INSERT INTO invoices VALUES (22, 'INV/2025/002', 4, '2025-02-01', '2025-03-01', 'unpaid', NULL, NULL, 'Pending approval');
INSERT INTO invoices VALUES (23, 'INV/2025/003', 2, '2025-03-15', '2025-04-15', 'unpaid', NULL, NULL, NULL);
INSERT INTO invoices VALUES (24, 'INV/2025/004', 7, '2025-01-20', '2025-02-20', 'paid', '2025-02-18', 'bank_transfer', 'Kubernetes setup');
INSERT INTO invoices VALUES (25, 'INV/2025/005', 8, '2025-02-10', '2025-03-10', 'paid', '2025-03-08', 'credit_card', 'Payment gateway integration');
INSERT INTO invoices VALUES (26, 'INV/2025/006', 9, '2025-03-01', '2025-04-01', 'unpaid', NULL, NULL, 'Inventory module');
INSERT INTO invoices VALUES (27, 'INV/2025/007', 10, '2025-03-20', '2025-04-20', 'draft', NULL, NULL, 'Phase 2 - pending review');
INSERT INTO invoices VALUES (28, 'INV/2025/008', 11, '2025-04-01', '2025-05-01', 'draft', NULL, NULL, 'Social media campaign');
INSERT INTO invoices VALUES (29, 'INV/2025/009', 12, '2025-04-10', '2025-05-10', 'unpaid', NULL, NULL, 'Demo day preparation');
INSERT INTO invoices VALUES (30, 'INV/2025/010', 1, '2025-05-01', '2025-06-01', 'draft', NULL, NULL, 'Q2 consulting hours');

-- 2026 Invoices (current year)
INSERT INTO invoices VALUES (31, 'INV/2026/001', 2, '2026-01-05', '2026-02-05', 'paid', '2026-02-01', 'bank_transfer', 'New year project kickoff');
INSERT INTO invoices VALUES (32, 'INV/2026/002', 6, '2026-01-15', '2026-02-15', 'paid', '2026-02-12', 'bank_transfer', 'Investment analysis tool');
INSERT INTO invoices VALUES (33, 'INV/2026/003', 7, '2026-02-01', '2026-03-01', 'unpaid', NULL, NULL, 'Monthly support retainer');
INSERT INTO invoices VALUES (34, 'INV/2026/004', 8, '2026-02-10', '2026-03-10', 'unpaid', NULL, NULL, 'API v2.0 development');
INSERT INTO invoices VALUES (35, 'INV/2026/005', 10, '2026-02-20', '2026-03-20', 'draft', NULL, NULL, 'Telemedicine features');

-- =====================
-- INSERT INVOICE ITEMS (EXPANDED)
-- =====================
-- Invoice 1
INSERT INTO invoice_items VALUES (1, 1, 'IT Consulting', 2, 10, 200.00, 0.23);
INSERT INTO invoice_items VALUES (2, 1, 'System Implementation', 1, 1, 5000.00, 0.23);
-- Invoice 2
INSERT INTO invoice_items VALUES (3, 2, 'Data Analysis', 4, 5, 300.00, 0.23);
-- Invoice 3
INSERT INTO invoice_items VALUES (4, 3, 'IT Consulting', 2, 8, 200.00, 0.23);
INSERT INTO invoice_items VALUES (5, 3, 'Code Review', 1, 3, 250.00, 0.23);
-- Invoice 4
INSERT INTO invoice_items VALUES (6, 4, 'Graphic Design', 5, 3, 400.00, 0.23);
-- Invoice 5
INSERT INTO invoice_items VALUES (7, 5, 'Python Training', 3, 2, 1500.00, 0.23);
-- Invoice 6
INSERT INTO invoice_items VALUES (8, 6, 'Data Engineering', 4, 6, 350.00, 0.23);
-- Invoice 7
INSERT INTO invoice_items VALUES (9, 7, 'ML Model Development', 4, 1, 8000.00, 0.23);
-- Invoice 8
INSERT INTO invoice_items VALUES (10, 8, 'IT Consulting', 2, 12, 200.00, 0.23);
-- Invoice 9
INSERT INTO invoice_items VALUES (11, 9, 'Database Optimization', 1, 4, 450.00, 0.23);
-- Invoice 10
INSERT INTO invoice_items VALUES (12, 10, 'Data Analysis', 4, 8, 300.00, 0.23);
-- Invoice 11
INSERT INTO invoice_items VALUES (13, 11, 'Python Training', 3, 3, 1500.00, 0.23);
-- Invoice 12
INSERT INTO invoice_items VALUES (14, 12, 'ML Model Development', 4, 1, 6000.00, 0.23);
-- Invoice 13
INSERT INTO invoice_items VALUES (15, 13, 'Investment Portfolio Analysis', 4, 10, 350.00, 0.23);
INSERT INTO invoice_items VALUES (16, 13, 'Technical Due Diligence', 2, 5, 400.00, 0.23);
-- Invoice 14
INSERT INTO invoice_items VALUES (17, 14, 'Cloud Architecture Design', 7, 1, 3000.00, 0.23);
INSERT INTO invoice_items VALUES (18, 14, 'AWS Migration', 7, 8, 250.00, 0.23);
-- Invoice 15
INSERT INTO invoice_items VALUES (19, 15, 'API Development', 1, 40, 180.00, 0.23);
INSERT INTO invoice_items VALUES (20, 15, 'Security Audit', 6, 1, 2500.00, 0.23);
-- Invoice 16
INSERT INTO invoice_items VALUES (21, 16, 'E-commerce Platform Setup', 1, 1, 8000.00, 0.23);
INSERT INTO invoice_items VALUES (22, 16, 'Payment Integration', 1, 15, 200.00, 0.23);
-- Invoice 17
INSERT INTO invoice_items VALUES (23, 17, 'Healthcare App Development', 1, 1, 12000.00, 0.23);
INSERT INTO invoice_items VALUES (24, 17, 'HIPAA Compliance Review', 2, 8, 300.00, 0.23);
-- Invoice 18
INSERT INTO invoice_items VALUES (25, 18, 'Website Redesign', 5, 1, 4500.00, 0.23);
INSERT INTO invoice_items VALUES (26, 18, 'SEO Optimization', 2, 10, 150.00, 0.23);
-- Invoice 19
INSERT INTO invoice_items VALUES (27, 19, 'Startup Mentoring', 3, 20, 200.00, 0.23);
INSERT INTO invoice_items VALUES (28, 19, 'Pitch Deck Review', 2, 5, 250.00, 0.23);
-- Invoice 20
INSERT INTO invoice_items VALUES (29, 20, 'Market Analysis Report', 4, 1, 5000.00, 0.23);
-- Invoice 21-35 (2025-2026)
INSERT INTO invoice_items VALUES (30, 21, 'IT Consulting', 2, 15, 200.00, 0.23);
INSERT INTO invoice_items VALUES (31, 22, 'Data Engineering', 4, 10, 350.00, 0.23);
INSERT INTO invoice_items VALUES (32, 23, 'System Implementation', 1, 1, 7000.00, 0.23);
INSERT INTO invoice_items VALUES (33, 24, 'Kubernetes Setup', 7, 1, 4500.00, 0.23);
INSERT INTO invoice_items VALUES (34, 24, 'DevOps Training', 3, 2, 1200.00, 0.23);
INSERT INTO invoice_items VALUES (35, 25, 'Payment Gateway API', 1, 30, 200.00, 0.23);
INSERT INTO invoice_items VALUES (36, 26, 'Inventory Management Module', 1, 1, 6500.00, 0.23);
INSERT INTO invoice_items VALUES (37, 27, 'Telemedicine Features', 1, 1, 9000.00, 0.23);
INSERT INTO invoice_items VALUES (38, 28, 'Social Media Dashboard', 1, 1, 5500.00, 0.23);
INSERT INTO invoice_items VALUES (39, 29, 'Demo Day App', 1, 1, 3000.00, 0.23);
INSERT INTO invoice_items VALUES (40, 30, 'Strategic Consulting', 2, 20, 220.00, 0.23);
INSERT INTO invoice_items VALUES (41, 31, 'Project Kickoff Workshop', 3, 2, 1800.00, 0.23);
INSERT INTO invoice_items VALUES (42, 32, 'Investment Analytics Tool', 1, 1, 7500.00, 0.23);
INSERT INTO invoice_items VALUES (43, 33, 'Monthly Support Retainer', 6, 1, 2500.00, 0.23);
INSERT INTO invoice_items VALUES (44, 34, 'API v2.0 Development', 1, 50, 190.00, 0.23);
INSERT INTO invoice_items VALUES (45, 35, 'Telemedicine v2 Features', 1, 1, 11000.00, 0.23);

-- =====================
-- INSERT PAYMENTS
-- =====================
INSERT INTO payments VALUES (1, 1, 8610.00, '2024-02-10', 'bank_transfer', 'TRX-2024-001');
INSERT INTO payments VALUES (2, 2, 1845.00, '2024-03-05', 'bank_transfer', 'TRX-2024-002');
INSERT INTO payments VALUES (3, 3, 2889.00, '2024-04-01', 'bank_transfer', 'TRX-2024-003');
INSERT INTO payments VALUES (4, 5, 3690.00, '2024-04-28', 'credit_card', 'CC-2024-001');
INSERT INTO payments VALUES (5, 6, 2583.00, '2024-06-08', 'bank_transfer', 'TRX-2024-004');
INSERT INTO payments VALUES (6, 7, 9840.00, '2024-07-12', 'bank_transfer', 'TRX-2024-005');
INSERT INTO payments VALUES (7, 10, 2952.00, '2024-10-02', 'bank_transfer', 'TRX-2024-006');
INSERT INTO payments VALUES (8, 11, 5535.00, '2024-11-10', 'bank_transfer', 'TRX-2024-007');
INSERT INTO payments VALUES (9, 13, 6765.00, '2024-06-28', 'bank_transfer', 'TRX-2024-008');
INSERT INTO payments VALUES (10, 14, 6150.00, '2024-08-12', 'bank_transfer', 'TRX-2024-009');
INSERT INTO payments VALUES (11, 15, 11931.00, '2024-08-29', 'credit_card', 'CC-2024-002');
INSERT INTO payments VALUES (12, 16, 13530.00, '2024-10-08', 'bank_transfer', 'TRX-2024-010');
INSERT INTO payments VALUES (13, 17, 17712.00, '2024-10-30', 'bank_transfer', 'TRX-2024-011');
INSERT INTO payments VALUES (14, 18, 7380.00, '2024-11-18', 'paypal', 'PP-2024-001');
INSERT INTO payments VALUES (15, 20, 6150.00, '2024-12-10', 'bank_transfer', 'TRX-2024-012');
INSERT INTO payments VALUES (16, 21, 3690.00, '2025-02-08', 'bank_transfer', 'TRX-2025-001');
INSERT INTO payments VALUES (17, 24, 8487.00, '2025-02-18', 'bank_transfer', 'TRX-2025-002');
INSERT INTO payments VALUES (18, 25, 7380.00, '2025-03-08', 'credit_card', 'CC-2025-001');
INSERT INTO payments VALUES (19, 31, 4428.00, '2026-02-01', 'bank_transfer', 'TRX-2026-001');
INSERT INTO payments VALUES (20, 32, 9225.00, '2026-02-12', 'bank_transfer', 'TRX-2026-002');

-- =====================
-- INSERT RECURRING TEMPLATES
-- =====================
INSERT INTO recurring_templates VALUES (1, 1, 'Monthly IT Support Retainer', 2500.00, 'monthly', '2026-03-01', 1);
INSERT INTO recurring_templates VALUES (2, 7, 'Cloud Infrastructure Support', 3000.00, 'monthly', '2026-03-01', 1);
INSERT INTO recurring_templates VALUES (3, 6, 'Quarterly Investment Analysis', 5000.00, 'quarterly', '2026-04-01', 1);
INSERT INTO recurring_templates VALUES (4, 10, 'Annual Healthcare App Maintenance', 15000.00, 'yearly', '2027-01-01', 1);
""")

conn.commit()
conn.close()
print("Database created successfully!")
print("Stats: 35 invoices, 12 customers, 45 line items, 20 payments")
print("New tables: service_categories, payments, recurring_templates")