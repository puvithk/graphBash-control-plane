import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

# Database configuration 
DATABASE_URL = os.getenv("DATABASE_URL") 

_engine = create_engine(DATABASE_URL , echo=True)


def get_session():
    with Session(_engine) as session:
        yield session


if __name__ == "__main__" :
    from app.db.migrations import run_db_migrations
    run_db_migrations(_engine)
