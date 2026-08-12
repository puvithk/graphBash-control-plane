import bcrypt


class PasswordUtils:
    def hash(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        return bcrypt.hashpw(pwd_bytes[:72], bcrypt.gensalt()).decode('utf-8')

    def verify(self, password: str, hashed_password: str) -> bool:
        if not password or not hashed_password:
            return False
        pwd_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        try:
            return bcrypt.checkpw(pwd_bytes[:72], hashed_bytes)
        except Exception:
            return False