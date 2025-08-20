from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"  # Use :memory: for tests if needed

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
