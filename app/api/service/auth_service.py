
from app.api.service.jwt_service import JwtService
from app.core.exception import InvalidCredentialsException
from app.core.exception import ValueNotFoundException
from app.api.dto.user_dto import UserSignInRequest, UserSignUpRequest, UserLoginResponse
from app.api.service.user_service import UserService
from ..utils.password import PasswordUtils
from ..schemas.user import User
jwt_service =  JwtService()

class AuthService:
    def __init__(self , session):
        self.session = session
        self.user_service = UserService(session)

    def signup(self , user : UserSignUpRequest):
        return self.user_service.create_user(user)

    def login(self , user_request : UserSignInRequest):
        db_user : User  = self.user_service.get_user_by_email(user_request.user_email)

        if not PasswordUtils().verify(user_request.user_password , db_user.user_hash):
            raise InvalidCredentialsException("Email or password is wrong")


        token = jwt_service.create_token(
            {
                "sub": str(db_user.user_id),
                "user_id": db_user.user_id,
                "email": db_user.user_email,
            }
        )

        return UserLoginResponse(token=token)



        