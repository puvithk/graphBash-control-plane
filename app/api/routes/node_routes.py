from typing import Annotated, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.schemas.node import NodeDetails
from app.core.database import get_session
from ..service.node_service import NodeService

route = APIRouter(prefix="/nodes", tags=["nodes"])

SessionDep = Annotated[Session, Depends(get_session)]


@route.get("/lists", response_model=List[NodeDetails])
def get_all_nodes(session: SessionDep):
    node_service = NodeService(session)
    return node_service.get_all_node()
