from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config

# Database configuration from config
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_DATABASE = config.DB_DATABASE
DB_USERNAME = config.DB_USERNAME
DB_PASSWORD = config.DB_PASSWORD

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
