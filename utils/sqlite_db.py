from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Global variables for lazy initialization
_engine = None
_SessionLocal = None

def get_engine():
    """Lazy initialization of database engine"""
    global _engine
    if _engine is None:
        # SQLite Database URL for development
        DATABASE_URL = "sqlite:///./reporting_app.db"
        
        # Create engine
        _engine = create_engine(
            DATABASE_URL,
            echo=True,
            connect_args={"check_same_thread": False}  # SQLite specific
        )
    return _engine

def get_session_local():
    """Lazy initialization of session maker"""
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=get_engine())