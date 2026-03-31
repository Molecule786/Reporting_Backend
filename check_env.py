"""
Quick diagnostic - add GET /debug/env endpoint temporarily
Run: python check_env.py to see what Railway sees
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Environment Variables on Railway ===")
print(f"MYSQL_HOST     : {os.getenv('MYSQL_HOST', 'NOT SET - using default: localhost')}")
print(f"MYSQL_PORT     : {os.getenv('MYSQL_PORT', 'NOT SET - using default: 3306')}")
print(f"MYSQL_USER     : {os.getenv('MYSQL_USER', 'NOT SET - using default: root')}")
print(f"MYSQL_PASSWORD : {'SET' if os.getenv('MYSQL_PASSWORD') else 'NOT SET - using default: empty'}")
print(f"MYSQL_DATABASE : {os.getenv('MYSQL_DATABASE', 'NOT SET - using default: reporting_db')}")
print(f"SECRET_KEY     : {'SET' if os.getenv('SECRET_KEY') else 'NOT SET'}")
print(f"PORT           : {os.getenv('PORT', 'NOT SET')}")
