from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    print("Database connection successful!")

SessionLocal = sessionmaker(bind=engine)

print(Base.metadata.tables.keys())
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

