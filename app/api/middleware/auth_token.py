
from fastapi import Depends, HTTPException, status
from app.api.routes.auth import oauth_bearer
from app.api.service.jwt_service import JwtService
from app.core.exception import InvalidCredentialsException

jwt_service = JwtService()


async def verify_auth_token(token: str = Depends(oauth_bearer)) -> dict:
    try:
        payload = jwt_service.verify_token(token)
        return payload
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )