
from uuid import uuid4
from datetime import datetime
from app.core.exception import ValueAlreadyExistsException
from app.api.repository.user_repo import UserRepositoy
from sqlalchemy.orm import Session
from ..dto.user_dto import UserSignUpRequest , UserSignUpResponse
from ..schemas.user import User
class UserService():


    def __init__(self , session : Session):
        self.session = session

    def create_user(self , user_request : UserSignUpRequest ):

        user_repo = UserRepositoy(self.session)

        if user_repo.get_user_by_email(user_request.user_email):
            raise ValueAlreadyExistsException("User already exists")


        user = User(
 
            user_name = user_request.user_name,
            user_email = user_request.user_email,
            user_hash = user_request.user_password,
            user_role = user_request.user_role,
            user_status = user_request.user_status,
            user_created_at = datetime.now(),
            user_updated_at = datetime.now()
        )
        

        user_repo.create_user(user)

        return UserSignUpResponse(
            user_name = user.user_name,
            user_email = user.user_email,
            user_role = user.user_role,
            user_status = user.user_status,
            user_created_at = user.user_created_at,
            user_updated_at = user.user_updated_at
        )