# MySQL Migration Setup Guide

## ✅ Migration Complete!

Your backend has been successfully migrated from MongoDB to MySQL (Hostinger).

## Database Configuration

**Hostinger MySQL Credentials:**
- Host: `auth-db1859.hstgr.io`
- Port: `3306`
- User: `u287952964_molecule`
- Password: `Conference786`
- Database: `u287952964_Reporting`

## Installation Steps

### 1. Install MySQL Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Test MySQL Connection
```bash
python test_mysql_connection.py
```

This will:
- Test connection to Hostinger MySQL
- Create all database tables automatically
- Verify everything is working

### 3. Run the Server
```bash
python run_server.py
```

Or for production:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## What Changed?

### ✅ Completed
- ✅ Removed all MongoDB dependencies
- ✅ Added MySQL/SQLAlchemy dependencies
- ✅ Created MySQL database models (User, Report, Task, Leave)
- ✅ Migrated all routes to MySQL:
  - auth.py (signup, login)
  - users.py (CRUD operations)
  - reports.py (CRUD operations)
  - tasks.py (CRUD operations)
  - dashboard.py (statistics)
  - leaves.py (leave management)
  - upload.py (file uploads)
  - export.py (data export)
  - password_reset.py (password recovery)
- ✅ Updated main.py for MySQL
- ✅ Configured .env with Hostinger credentials

### Database Tables Created
1. **users** - User accounts (admin/employee)
2. **reports** - Daily reports with attachments
3. **tasks** - Task assignments
4. **leaves** - Leave requests

## API Endpoints

All endpoints remain the same:
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/users/me` - Get current user
- `POST /api/reports` - Create report
- `GET /api/reports` - Get all reports
- `POST /api/tasks` - Create task
- `GET /api/tasks` - Get all tasks
- `POST /api/leaves` - Request leave
- `GET /api/leaves` - Get leaves
- `GET /api/dashboard/stats` - Dashboard statistics

## Troubleshooting

### Connection Error
If you get connection errors:
1. Check Hostinger database is active
2. Verify credentials in `.env` file
3. Check if your IP is whitelisted in Hostinger
4. Try accessing phpMyAdmin: https://auth-db1859.hstgr.io/

### Table Creation Error
If tables don't create:
1. Login to phpMyAdmin
2. Manually create tables using SQL from `init_mysql_db.py`
3. Or drop and recreate the database

### Import Errors
If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Testing

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Test User","email":"test@example.com","password":"test123","role":"employee"}'
```

### Test Health
```bash
curl http://localhost:8000/health
```

## Deployment to Railway

Your Procfile is already configured. Just push to GitHub:

```bash
git add .
git commit -m "Migrated to MySQL"
git push origin main
```

Railway will automatically:
1. Install MySQL dependencies
2. Connect to Hostinger MySQL
3. Create tables on first run
4. Start the server

## Need Help?

- Check logs: `python run_server.py`
- Test connection: `python test_mysql_connection.py`
- View tables in phpMyAdmin: https://auth-db1859.hstgr.io/

## Success! 🎉

Your application is now running on MySQL with Hostinger!
