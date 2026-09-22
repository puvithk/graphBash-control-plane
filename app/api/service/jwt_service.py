from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_TIME, ALGORITHM, SECRET_KEY
from app.core.exception import InvalidCredentialsException


class JwtService:

    """
    JWT Service to Access the secured resources
    """
    def create_token(self , data : dict , expire_time : int = ACCESS_TOKEN_EXPIRE_TIME ):
        #Make a copy of the data which will ahve sub & iat 
        to_encode = data.copy()
        # Get the token expire time 
        token_expire_time =  datetime.now(UTC) + timedelta(minutes=expire_time)

        #Update the expiration time 
        to_encode.update({"exp" : token_expire_time})
        #Encode into Token and sign it 
        encode_token = self._encode(to_encode)
        #Return the token if valid
        return encode_token     
    

    def verify_token(self , token : str ):
        #Verify the token 
        try:
            payload : dict = self._decode(token)
            return payload
        except jwt.PyJWTError as e:
            raise InvalidCredentialsException(f"Invalid or expired token: {e!s}")

    def _encode(self , payload : dict):
        
        return jwt.encode(payload , SECRET_KEY , algorithm=ALGORITHM)

    def _decode(self , token : str):
        return jwt.decode(token ,SECRET_KEY, algorithms=[ALGORITHM])
