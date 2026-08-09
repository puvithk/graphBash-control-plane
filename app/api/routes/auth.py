


from app.core.database import get_session
from fastapi import Depends
from sqlalchemy.util.typing import Annotated
from sqlalchemy.orm import Session
from sys import prefix
from fastapi import APIRouter
route = APIRouter(prefix="/auth" , tags=["nodes"])

SessionDep = Annotated[Session ,  Depends(get_session)]

