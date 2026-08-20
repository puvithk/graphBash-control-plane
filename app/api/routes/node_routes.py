from app.api.dto.node_dto import NodeRegistrationTokenRequest
from app.api.dto.node_dto import NodeRegistrationResponse
from app.api.dto.node_dto import NodeRegistrationToken
from fastapi import status
from fastapi import HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.dto.node_dto import NodeRequestDTO
from app.api.schemas.node import NodeDetails
from app.core.database import get_session
from ..service.node_service import NodeService
from app.api.middleware.auth_token import verify_auth_token, CurrentUser
route = APIRouter(
    prefix="/nodes",
    tags=["nodes"],
    dependencies=[Depends(verify_auth_token)],
)

SessionDep = Annotated[Session, Depends(get_session)]


@route.get("/lists", response_model=List[NodeDetails])
def get_all_nodes(session: SessionDep, current_user: CurrentUser):
    node_service = NodeService(session)
    owner_id = current_user.get("user_id")
    if owner_id is None and current_user.get("sub"):
        owner_id = int(current_user.get("sub"))

    if owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return node_service.get_all_node(owner_id)


@route.get("/{node_id}", response_model=NodeDetails)
def get_node_by_id(session: SessionDep, node_id: str , current_user : CurrentUser):
    node_service = NodeService(session)
    owner_id = current_user.get("user_id")
    if owner_id is None and current_user.get("sub"):
        owner_id = int(current_user.get("sub"))

    if owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    node = node_service.get_node_by_id(node_id, owner_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Node with ID '{node_id}' not found"
        )
    return node


@route.post("/create", response_model=NodeDetails)
def create_node(session: SessionDep, node_request: NodeRequestDTO , current_user : CurrentUser):
    node_service = NodeService(session)

    owner_id = current_user.get("user_id")
    if owner_id is None and current_user.get("sub"):
        owner_id = int(current_user.get("sub"))

    if owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )


    return node_service.create_node(node_request=node_request , owner_id = owner_id)




@route.post("/node-registration-request" , response_model=NodeRegistrationToken)
def node_registration_request(session : SessionDep , node_request : NodeRequestDTO , current_user : CurrentUser):
    node_service = NodeService(session)

    owner_id = current_user.get("user_id")
    if owner_id is None and current_user.get("sub"):
        owner_id = int(current_user.get("sub"))

    if owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try : 
        node_registration_token = node_service.node_registration_request(node_request=node_request , owner_id = owner_id)
    except Exception as e : 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return node_registration_token


@route.post("/node-registration" , response_model = NodeRegistrationResponse )
def node_registration(session : SessionDep , node_request : NodeRegistrationTokenRequest):
    node_service = NodeService(session)
    try :
        node_registration = node_service.node_registration(node_request=node_request)
    except Exception as e :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return node_registration