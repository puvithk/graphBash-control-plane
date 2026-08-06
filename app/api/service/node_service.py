

from app.api.schemas.node import NodeDetails
from typing import List
from sqlalchemy.orm import Session
from ..repository.node_repo import NodeRepository
class NodeService():

    def __init__(self , session : Session):
        self.session = session


    def get_all_node(self) -> List[NodeDetails]:
        
        node_repo = NodeRepository(self.session)
        node_list = node_repo.get_all_nodees()
        return node_list
