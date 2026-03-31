from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from utils.mysql_db import Base, get_engine, init_db
from models_mysql.user import User
from models_mysql.report import Report
from models_mysql.task import Task
from models_mysql.leave import Leave

# Import MySQL routes
from routes_mysql import auth, users, reports, tasks, dashboard, leaves, password_reset, upload, export, chat

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        print("[INFO] Initializing MySQL database connection...")
        # Create all tables if they don't exist
        Base.metadata.create_all(bind=get_engine())
        print("[SUCCESS] MySQL database connected and tables initialized")
        print("[INFO] Database tables: users, reports, tasks, leaves")
    except Exception as e:
        print(f"[ERROR] Database initialization error: {e}")
        print("[WARNING] Server starting without database connection")
    
    yield
    
    # Shutdown
    print("[INFO] Shutting down application")

app = FastAPI(title="Molecule WorkFlow Pro API", lifespan=lifespan, redirect_slashes=False)

# CORS middleware configuration - Allow only specific production domains
origins = [
    "https://mediumblue-dogfish-255821.hostingersite.com",  # Hostinger frontend
    "http://mediumblue-dogfish-255821.hostingersite.com", 
    "https://reporting.webconferencesolutions.com",  # Another valid domain
    "http://localhost:3000",  # For local development (React or Vue frontend)
    "http://localhost:8000",  # For local FastAPI testing
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for various API routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(leaves.router, prefix="/api/leaves", tags=["Leaves"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(password_reset.router, prefix="/api/auth", tags=["Password Reset"])
app.include_router(export.router, prefix="/api/export", tags=["Export"])
app.include_router(chat.router, prefix="/api/chat", tags=["AI Chatbot"])

@app.get("/")
async def root():
    return {"message": "Molecule WorkFlow Pro API - MySQL", "status": "running"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint for general health and database connection"""
    try:
        # Check if the database connection is healthy
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")  # Simple query to check DB connection
        return {"status": "ok", "message": "Server is running with MySQL"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {e}"}

@app.get("/health")
async def health_check_root():
    """Health check endpoint for Railway to check server status"""
    return {"status": "ok", "message": "Server is running with MySQL"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))  # Use environment variable for port, default to 8001
    uvicorn.run(app, host="0.0.0.0", port=port)