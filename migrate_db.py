import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from utils.mysql_db import get_engine

def migrate_reports_table():
    engine = get_engine()
    with engine.begin() as conn:
        try:
            print("Running migration...")
            
            # Catch errors if columns don't exist
            try:
                conn.execute(text("ALTER TABLE reports DROP COLUMN title;"))
                print("Dropped title column")
            except Exception as e:
                print(f"title column might not exist: {e}")
                
            try:
                conn.execute(text("ALTER TABLE reports DROP COLUMN priority;"))
                print("Dropped priority column")
            except Exception as e:
                print(f"priority column might not exist: {e}")
                
            try:
                conn.execute(text("ALTER TABLE reports DROP COLUMN category;"))
                print("Dropped category column")
            except Exception as e:
                print(f"category column might not exist: {e}")
            
            # Add new columns
            try:
                conn.execute(text("ALTER TABLE reports ADD COLUMN project_name VARCHAR(255);"))
                print("Added project_name column")
            except Exception as e:
                print(f"project_name might already exist: {e}")
                
            try:
                conn.execute(text("ALTER TABLE reports ADD COLUMN project_code VARCHAR(100);"))
                print("Added project_code column")
            except Exception as e:
                print(f"project_code might already exist: {e}")
            
            print("Migration completed!")
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == '__main__':
    migrate_reports_table()
