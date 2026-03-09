"""
Initialize MySQL Database Tables
Run this script once to create all tables in your Hostinger MySQL database
"""

from utils.mysql_db import engine, Base, init_db
from models_mysql.user import User
from models_mysql.report import Report
from models_mysql.task import Task
from models_mysql.leave import Leave

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ All tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - reports")
        print("  - tasks")
        print("  - leaves")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    create_tables()
