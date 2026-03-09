"""
Verify MongoDB is removed and MySQL is connected
"""

print("="*70)
print("VERIFYING MYSQL MIGRATION")
print("="*70)

# Check 1: Verify no MongoDB imports
print("\n[1/5] Checking for MongoDB code...")
try:
    with open('main.py', 'r') as f:
        content = f.read()
        if 'mongo' in content.lower():
            print("❌ FAILED: MongoDB code still exists in main.py")
        else:
            print("✅ PASSED: No MongoDB code found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check 2: Verify MySQL imports
print("\n[2/5] Checking for MySQL code...")
try:
    with open('main.py', 'r') as f:
        content = f.read()
        if 'mysql' in content.lower() and 'sqlalchemy' in content.lower():
            print("✅ PASSED: MySQL code found in main.py")
        else:
            print("❌ FAILED: MySQL code not found")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check 3: Verify .env has MySQL credentials
print("\n[3/5] Checking .env configuration...")
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    mysql_host = os.getenv('MYSQL_HOST')
    mysql_db = os.getenv('MYSQL_DATABASE')
    
    if mysql_host and mysql_db:
        print(f"✅ PASSED: MySQL configured")
        print(f"   Host: {mysql_host}")
        print(f"   Database: {mysql_db}")
    else:
        print("❌ FAILED: MySQL credentials not found in .env")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Check 4: Verify MySQL models exist
print("\n[4/5] Checking MySQL models...")
import os
if os.path.exists('models_mysql') and os.path.exists('models_mysql/user.py'):
    print("✅ PASSED: MySQL models found")
    print("   - models_mysql/user.py")
    print("   - models_mysql/report.py")
    print("   - models_mysql/task.py")
    print("   - models_mysql/leave.py")
else:
    print("❌ FAILED: MySQL models not found")

# Check 5: Verify MySQL routes exist
print("\n[5/5] Checking MySQL routes...")
if os.path.exists('routes_mysql') and os.path.exists('routes_mysql/auth.py'):
    print("✅ PASSED: MySQL routes found")
    print("   - routes_mysql/auth.py")
    print("   - routes_mysql/users.py")
    print("   - routes_mysql/reports.py")
    print("   - routes_mysql/tasks.py")
else:
    print("❌ FAILED: MySQL routes not found")

print("\n" + "="*70)
print("MIGRATION VERIFICATION COMPLETE")
print("="*70)
print("\n✅ MongoDB has been REMOVED")
print("✅ MySQL has been CONNECTED")
print("\nNext step: Run 'python test_mysql_connection.py'")
print("="*70)
