# Backend Deployment Guide for Hostinger

## Prerequisites
- Your backend files are ready
- Database is configured and accessible
- Hostinger hosting account with Python support

## Deployment Steps

### 1. Upload Backend Files
Upload all backend files to your Hostinger hosting directory:
- main.py
- requirements.txt
- .env (with your database credentials)
- models_mysql/ folder
- routes_mysql/ folder  
- utils/ folder

### 2. Install Dependencies
In your Hostinger terminal/file manager, run:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Make sure your .env file has the correct database settings:
```
MYSQL_HOST=31.97.208.72
MYSQL_PORT=3306
MYSQL_USER=u811751330_Molecule
MYSQL_PASSWORD=Molecule5643
MYSQL_DATABASE=u811751330_Reporting
```

### 4. Start the Application
Run the FastAPI application:
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 5. Test the Backend
Your backend should be accessible at:
- https://your-backend-domain.hostingersite.com
- Or subdomain you configure

## Frontend Configuration
Update the frontend API service to point to your deployed backend:
```dart
static String baseUrl = 'https://your-backend-domain.hostingersite.com/api';
```

## Important Notes
- Make sure your database IP whitelist includes your backend server IP
- Update CORS settings to include your frontend domain
- Test all endpoints after deployment