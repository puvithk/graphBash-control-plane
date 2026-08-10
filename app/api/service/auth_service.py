
from app.core.exception import InvalidCredentialsException
from app.core.exception import ValueNotFoundException
from app.api.dto.user_dto import UserSignInRequest, UserSignUpRequest, UserLoginResponse
from app.api.service.user_service import UserService

class AuthService:
    def __init__(self , session):
        self.session = session
        self.user_service = UserService(session)

    def signup(self , user : UserSignUpRequest):
        return self.user_service.create_user(user)

    def login(self , user_request : UserSignInRequest):
        db_user = self.user_service.get_user_by_email(user_request.user_email)

        if db_user.user_hash != user_request.user_password:
            raise InvalidCredentialsException("Email or password is wrong")

        return UserLoginResponse(token="dummy_token")



        