


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.util.typing import Annotated

from app.api.dto.user_dto import (
    UserLoginResponse,
    UserSignInRequest,
    UserSignUpRequest,
    UserSignUpResponse,
)
from app.api.service.auth_service import AuthService
from app.core.database import get_session
from app.core.exception import InvalidCredentialsException, ValueNotFoundException

route = APIRouter(prefix="/auth" , tags=["auth"])

SessionDep = Annotated[Session ,  Depends(get_session)]



@route.post("/signup" , response_model= UserSignUpResponse)
def signup( session : SessionDep, user : UserSignUpRequest):
    auth_service = AuthService(session)
    return auth_service.signup(user)

@route.post(
    "/login",
    response_model=UserLoginResponse,
    responses={
        401: {"description": "Invalid credentials"},
    },
)
def login( session : SessionDep , user : UserSignInRequest):
    admin_service = AuthService(session)
    try :
        return admin_service.login(user)
    except InvalidCredentialsException:
        raise HTTPException(status_code=401 , detail="Invalid credentials")
    except ValueNotFoundException:
        raise HTTPException(status_code=401 , detail="Invalid credentials")