
from functools import wraps
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api.service.jwt_service import JwtService
from app.core.exception import InvalidCredentialsException

security = HTTPBearer()
jwt_service = JwtService()


def _verify_token_payload(token: str) -> dict:
    try:
        return jwt_service.verify_token(token)
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def verify_auth_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    return _verify_token_payload(credentials.credentials)


# Production Type Alias for Dependency Injection in Route Handlers
CurrentUser = Annotated[dict, Depends(verify_auth_token)]


def _extract_request(args: tuple, kwargs: dict) -> Request:
    request = kwargs.get("request")
    if not request:
        for arg in args:
            if isinstance(arg, Request):
                return arg

    if not request:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "@require_auth decorator requires 'request: Request' "
                "in endpoint signature."
            ),
        )
    return request


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_header.split(" ")[1]


def require_auth(func):
    """
    Decorator to protect FastAPI endpoints with JWT auth.
    Note: The decorated endpoint MUST include `request: Request`
    in its parameters.
    Example:
        @route.get("/example")
        @require_auth
        async def example_endpoint(request: Request):
            user = request.state.user
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = _extract_request(args, kwargs)
        token = _extract_bearer_token(request)
        request.state.user = _verify_token_payload(token)
        return await func(*args, **kwargs)

    return wrapper
