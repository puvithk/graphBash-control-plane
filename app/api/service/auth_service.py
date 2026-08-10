
from app.api.service.user_service import UserService
from app.api.dto.user_dto import UserSignUpRequest
class AuthService:
    def __init__(self , session):
        self.session = session
        self.user_service = UserService(session)

    def signup(self , user : UserSignUpRequest):
        return self.user_service.create_user(user)