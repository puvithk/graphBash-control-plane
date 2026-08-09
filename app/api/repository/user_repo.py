from sqlalchemy.orm import Session
from ..schemas.user import User
class UserRepositoy:
    def __init__(self , session : Session):
        self.session = session

    def get_user_by_email(self , email : str):
        return self.session.query(User).filter(User.user_email == email).first()
    
    def create_user(self , user : User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user