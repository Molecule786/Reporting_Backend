"""
Test MySQL Connection and Create Tables
Run this to verify your Hostinger MySQL database is working
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("Testing MySQL Connection to Hostinger")
print("="*60)

# Print configuration (hide password)
print(f"\nHost: {os.getenv('MYSQL_HOST')}")
print(f"Port: {os.getenv('MYSQL_PORT')}")
print(f"User: {os.getenv('MYSQL_USER')}")
print(f"Database: {os.getenv('MYSQL_DATABASE')}")
print(f"Password: {'*' * len(os.getenv('MYSQL_PASSWORD', ''))}")

try:
    print("\n[1/3] Importing MySQL utilities...")
    from utils.mysql_db import engine, Base
    print("✓ Import successful")
    
    print("\n[2/3] Testing database connection...")
    connection = engine.connect()
    print("✓ Connection successful!")
    connection.close()
    
    print("\n[3/3] Creating database tables...")
    from models_mysql.user import User
    from models_mysql.report import Report
    from models_mysql.task import Task
    from models_mysql.leave import Leave
    
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")
    
    print("\n" + "="*60)
    print("SUCCESS! MySQL Database is ready")
    print("="*60)
    print("\nTables created:")
    print("  ✓ users")
    print("  ✓ reports")
    print("  ✓ tasks")
    print("  ✓ leaves")
    print("\nYou can now run: python run_server.py")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Check your .env file has correct MySQL credentials")
    print("2. Verify Hostinger database is active")
    print("3. Check if your IP is allowed in Hostinger")
    print("4. Install dependencies: pip install -r requirements.txt")
    import traceback
    traceback.print_exc()
