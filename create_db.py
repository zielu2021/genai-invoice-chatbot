import sqlite3

conn = sqlite3.connect("invoices.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    nip TEXT,
    email TEXT,
    city TEXT,
    country TEXT DEFAULT 'Poland'
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    number TEXT NOT NULL,
    customer_id INTEGER,
    issue_date TEXT,
    due_date TEXT,
    status TEXT CHECK(status IN ('paid', 'unpaid', 'overdue')),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS invoice_items (
    id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    description TEXT,
    quantity REAL,
    unit_price REAL,
    vat_rate REAL DEFAULT 0.23,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id)
);

INSERT INTO customers VALUES (1, 'ABC Solutions Ltd.', '1234567890', 'abc@solutions.com', 'Warsaw', 'Poland');
INSERT INTO customers VALUES (2, 'XYZ Tech', '0987654321', 'xyz@tech.com', 'Krakow', 'Poland');
INSERT INTO customers VALUES (3, 'John Smith Consulting', '1122334455', 'john@smith.com', 'Gdansk', 'Poland');
INSERT INTO customers VALUES (4, 'DataFlow GmbH', '9876543210', 'contact@dataflow.de', 'Berlin', 'Germany');
INSERT INTO customers VALUES (5, 'Nordic Analytics', '5544332211', 'hello@nordic.se', 'Stockholm', 'Sweden');

INSERT INTO invoices VALUES (1,  'INV/2024/01', 1, '2024-01-15', '2024-02-15', 'paid');
INSERT INTO invoices VALUES (2,  'INV/2024/02', 2, '2024-02-10', '2024-03-10', 'paid');
INSERT INTO invoices VALUES (3,  'INV/2024/03', 1, '2024-03-05', '2024-04-05', 'paid');
INSERT INTO invoices VALUES (4,  'INV/2024/04', 3, '2024-03-20', '2024-04-20', 'overdue');
INSERT INTO invoices VALUES (5,  'INV/2024/05', 2, '2024-04-01', '2024-05-01', 'paid');
INSERT INTO invoices VALUES (6,  'INV/2024/06', 4, '2024-05-10', '2024-06-10', 'paid');
INSERT INTO invoices VALUES (7,  'INV/2024/07', 5, '2024-06-15', '2024-07-15', 'paid');
INSERT INTO invoices VALUES (8,  'INV/2024/08', 1, '2024-07-01', '2024-08-01', 'unpaid');
INSERT INTO invoices VALUES (9,  'INV/2024/09', 3, '2024-08-20', '2024-09-20', 'unpaid');
INSERT INTO invoices VALUES (10, 'INV/2024/10', 4, '2024-09-05', '2024-10-05', 'paid');
INSERT INTO invoices VALUES (11, 'INV/2024/11', 2, '2024-10-12', '2024-11-12', 'paid');
INSERT INTO invoices VALUES (12, 'INV/2024/12', 5, '2024-11-01', '2024-12-01', 'overdue');
INSERT INTO invoices VALUES (13, 'INV/2025/01', 1, '2025-01-10', '2025-02-10', 'paid');
INSERT INTO invoices VALUES (14, 'INV/2025/02', 4, '2025-02-01', '2025-03-01', 'unpaid');
INSERT INTO invoices VALUES (15, 'INV/2025/03', 2, '2025-03-15', '2025-04-15', 'unpaid');

INSERT INTO invoice_items VALUES (1,  1,  'IT Consulting',          10, 200.00, 0.23);
INSERT INTO invoice_items VALUES (2,  1,  'System Implementation',   1, 5000.00, 0.23);
INSERT INTO invoice_items VALUES (3,  2,  'Data Analysis',           5, 300.00, 0.23);
INSERT INTO invoice_items VALUES (4,  3,  'IT Consulting',           8, 200.00, 0.23);
INSERT INTO invoice_items VALUES (5,  3,  'Code Review',             3, 250.00, 0.23);
INSERT INTO invoice_items VALUES (6,  4,  'Graphic Design',          3, 400.00, 0.23);
INSERT INTO invoice_items VALUES (7,  5,  'Python Training',         2, 1500.00, 0.23);
INSERT INTO invoice_items VALUES (8,  6,  'Data Engineering',        6, 350.00, 0.23);
INSERT INTO invoice_items VALUES (9,  7,  'ML Model Development',    1, 8000.00, 0.23);
INSERT INTO invoice_items VALUES (10, 8,  'IT Consulting',          12, 200.00, 0.23);
INSERT INTO invoice_items VALUES (11, 9,  'Database Optimization',   4, 450.00, 0.23);
INSERT INTO invoice_items VALUES (12, 10, 'Data Analysis',           8, 300.00, 0.23);
INSERT INTO invoice_items VALUES (13, 11, 'Python Training',         3, 1500.00, 0.23);
INSERT INTO invoice_items VALUES (14, 12, 'ML Model Development',    1, 6000.00, 0.23);
INSERT INTO invoice_items VALUES (15, 13, 'IT Consulting',          15, 200.00, 0.23);
INSERT INTO invoice_items VALUES (16, 14, 'Data Engineering',       10, 350.00, 0.23);
INSERT INTO invoice_items VALUES (17, 15, 'System Implementation',   1, 7000.00, 0.23);
""")

conn.commit()
conn.close()
print("Database created successfully! 15 invoices, 5 customers.")