from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .job import Base
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/jobs.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database by creating all tables"""
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # If tables already exist, that's okay - just log and continue
        print(f"Note: Some tables may already exist: {e}")
        pass

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

