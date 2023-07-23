import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()