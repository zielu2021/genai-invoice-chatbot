-- Clients table
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    unit_price DECIMAL(10,2) NOT NULL,
    category TEXT
);

-- Invoices table
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    client_id INTEGER,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status TEXT DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    notes TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);

-- Invoice items table
CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Payment history table
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);

-- Insert clients
INSERT INTO clients (name, email, phone, address) VALUES
('Acme Corporation', 'billing@acme.com', '+1-555-0101', '123 Business Ave, New York, NY 10001'),
('TechStart Inc', 'accounts@techstart.io', '+1-555-0102', '456 Innovation Blvd, San Francisco, CA 94102'),
('Global Traders Ltd', 'finance@globaltraders.com', '+1-555-0103', '789 Commerce St, Chicago, IL 60601'),
('Digital Solutions', 'payments@digitalsol.com', '+1-555-0104', '321 Tech Park, Austin, TX 78701'),
('Green Energy Co', 'accounting@greenenergy.com', '+1-555-0105', '555 Eco Drive, Seattle, WA 98101'),
('Smart Retail Group', 'invoices@smartretail.com', '+1-555-0106', '888 Market St, Boston, MA 02101'),
('Healthcare Plus', 'billing@healthcareplus.com', '+1-555-0107', '999 Medical Center Dr, Miami, FL 33101'),
('Construction Pro', 'accounts@constructpro.com', '+1-555-0108', '777 Builder Lane, Denver, CO 80201');

-- Insert products
INSERT INTO products (name, description, unit_price, category) VALUES
('Web Development - Basic', 'Basic website development package', 1500.00, 'Development'),
('Web Development - Premium', 'Premium website with advanced features', 3500.00, 'Development'),
('Mobile App Development', 'Cross-platform mobile application', 5000.00, 'Development'),
('SEO Optimization', 'Search engine optimization service', 800.00, 'Marketing'),
('Social Media Management', 'Monthly social media management', 600.00, 'Marketing'),
('Cloud Hosting - Basic', 'Basic cloud hosting per month', 99.00, 'Hosting'),
('Cloud Hosting - Enterprise', 'Enterprise cloud hosting per month', 499.00, 'Hosting'),
('Technical Support - Hours', 'Technical support per hour', 75.00, 'Support'),
('Consulting - Strategy', 'Business strategy consulting per hour', 150.00, 'Consulting'),
('UI/UX Design', 'User interface and experience design', 2000.00, 'Design'),
('Logo Design', 'Professional logo design package', 500.00, 'Design'),
('Content Writing', 'Professional content writing per article', 100.00, 'Content'),
('Video Production', 'Professional video production', 1500.00, 'Content'),
('Data Analytics Setup', 'Analytics dashboard setup', 1200.00, 'Analytics'),
('Security Audit', 'Comprehensive security audit', 2500.00, 'Security');

-- Insert invoices
INSERT INTO invoices (invoice_number, client_id, issue_date, due_date, status, total_amount, notes) VALUES
('INV-2024-001', 1, '2024-01-15', '2024-02-15', 'paid', 5300.00, 'Website redesign project'),
('INV-2024-002', 2, '2024-01-20', '2024-02-20', 'paid', 5600.00, 'Mobile app phase 1'),
('INV-2024-003', 3, '2024-02-01', '2024-03-01', 'paid', 1400.00, 'Marketing services'),
('INV-2024-004', 4, '2024-02-10', '2024-03-10', 'overdue', 3500.00, 'Premium website development'),
('INV-2024-005', 5, '2024-02-15', '2024-03-15', 'pending', 2800.00, 'Consulting and design'),
('INV-2024-006', 1, '2024-03-01', '2024-04-01', 'paid', 1598.00, 'Monthly hosting and support'),
('INV-2024-007', 6, '2024-03-10', '2024-04-10', 'pending', 4200.00, 'E-commerce development'),
('INV-2024-008', 7, '2024-03-15', '2024-04-15', 'pending', 3700.00, 'Healthcare portal'),
('INV-2024-009', 2, '2024-03-20', '2024-04-20', 'draft', 5000.00, 'Mobile app phase 2'),
('INV-2024-010', 8, '2024-03-25', '2024-04-25', 'pending', 2500.00, 'Security audit'),
('INV-2024-011', 3, '2024-04-01', '2024-05-01', 'draft', 1800.00, 'Content and SEO'),
('INV-2024-012', 4, '2024-04-05', '2024-05-05', 'cancelled', 1500.00, 'Project cancelled by client');

-- Insert invoice items
INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price) VALUES
(1, 2, 1, 3500.00), (1, 4, 1, 800.00), (1, 11, 2, 500.00),
(2, 3, 1, 5000.00), (2, 5, 1, 600.00),
(3, 4, 1, 800.00), (3, 5, 1, 600.00),
(4, 2, 1, 3500.00),
(5, 9, 8, 150.00), (5, 10, 1, 2000.00), (5, 11, 1, 500.00),
(6, 7, 1, 499.00), (6, 6, 1, 99.00), (6, 8, 10, 75.00), (6, 12, 2, 100.00),
(7, 1, 1, 1500.00), (7, 10, 1, 2000.00), (7, 14, 1, 1200.00),
(8, 2, 1, 3500.00), (8, 14, 1, 1200.00),
(9, 3, 1, 5000.00),
(10, 15, 1, 2500.00),
(11, 12, 10, 100.00), (11, 4, 1, 800.00),
(12, 1, 1, 1500.00);

-- Insert payments
INSERT INTO payments (invoice_id, amount, payment_date, payment_method) VALUES
(1, 5300.00, '2024-02-10', 'bank_transfer'),
(2, 5600.00, '2024-02-18', 'credit_card'),
(3, 1400.00, '2024-02-28', 'bank_transfer'),
(6, 1598.00, '2024-03-28', 'credit_card');
