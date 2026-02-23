import sqlite3
import os

def init_database():
    """Initialize the database with schema and seed data."""
    db_path = "database/invoices.db"
    seed_path = "database/seed_data.sql"
    
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove existing database for fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    
    # Read and execute seed data
    with open(seed_path, 'r') as f:
        sql_script = f.read()
    
    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print(f"📁 Database location: {os.path.abspath(db_path)}")

if __name__ == "__main__":
    init_database()
