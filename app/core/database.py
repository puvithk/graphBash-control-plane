from functools import lru_cache
from sqlmodel import create_engine , Session , SQLModel

from ..api.schemas.node import NodeDetails , NodeCredential , NodeLifeCycle
from dotenv import load_dotenv

import os 
load_dotenv()

# Database configuration 

DATABASE_URL  = os.getenv("DATABASE_URL") 



_engine = create_engine(DATABASE_URL , echo=True)




def get_session():
    with Session(_engine) as session:
        yield session


if __name__ == "__main__" :
    SQLModel.metadata.create_all(_engine)
    print("Database tables created successfully")
        
    
        