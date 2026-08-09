


from app.api.service.user_service import UserService
from app.api.service import user_service
from app.api.dto.user_dto import UserSignUpRequest
from app.api.dto.user_dto import UserSignInRequest
from app.api.dto.user_dto import UserSignUpResponse
from app.core.database import get_session
from fastapi import Depends
from sqlalchemy.util.typing import Annotated
from sqlalchemy.orm import Session
from sys import prefix
from fastapi import APIRouter


route = APIRouter(prefix="/auth" , tags=["auth"])

SessionDep = Annotated[Session ,  Depends(get_session)]



@route.post("/signup" , response_model= UserSignUpResponse)
def signup(self , session : SessionDep, user : UserSignUpRequest):
    user_service = UserService(session)
    return user_service.create_user(user_request=user)