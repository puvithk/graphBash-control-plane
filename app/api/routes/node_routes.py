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
def get_all_nodes(session: SessionDep):
    node_service = NodeService(session)
    return node_service.get_all_node()


@route.get("/{node_id}", response_model=NodeDetails)
def get_node_by_id(session: SessionDep, node_id: str):
    node_service = NodeService(session)
    return node_service.get_node_by_id(node_id)


@route.post("/create", response_model=NodeDetails)
def create_node(session: SessionDep, node_request: NodeRequestDTO):
    node_service = NodeService(session)
    return node_service.create_node(node_request=node_request)

