


from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class User(SQLModel , table=True):

    user_id : int = Field(default=None , primary_key=True)
    
    user_name : str = Field(default=None , index=True)
    
    user_email : str = Field(default=None , index=True)

    user_salt : str | None = Field(default=None)
    
    user_hash : str | None = Field(default=None)
    
    user_role : UserRole = Field(default=None , index=True)
    
    user_created_at : datetime = Field(default=None , index=True)
    
    user_updated_at : datetime = Field(default=None , index=True)
    
    user_status : UserStatus = Field(default=None , index=True)
    

