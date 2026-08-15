

from sqlalchemy.engine import default
from app.api.schemas.user import UserStatus
from pydantic import BaseModel , Field
from datetime import datetime
class UserSignUpRequest(BaseModel):

    user_name : str = Field(default=None )
    user_email : str = Field(default=None)
    user_password : str = Field(default=None)
    user_role : str = Field(default=None)
    user_status : UserStatus  = Field(default=None)
    

class UserSignInRequest(BaseModel):

    user_email : str = Field(default=None)
    user_password : str = Field(default=None)


class UserSignUpResponse(BaseModel):
    user_id : str = Field(default=None)
    user_name : str = Field(default=None)
    user_email : str = Field(default=None)
    user_role : str = Field(default=None)
    user_status : UserStatus  = Field(default=None)
    user_created_at : datetime = Field(default=None)
    user_updated_at : datetime = Field(default=None)

class UserLoginResponse(BaseModel):

    token : str = Field(default=None , description="JWT ir session token after login")
    