from functools import lru_cache
from sqlmodel import create_engine , Session , SQLModel

from ..api.schemas.node import NodeDetails , NodeCredential , NodeRegisterDetails, NodeLifeCycle
from ..api.schemas.user import User
from dotenv import load_dotenv

import os 
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