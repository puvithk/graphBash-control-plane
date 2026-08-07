from sqlalchemy import select
from app.api.schemas.node import NodeDetails
from typing import List
from sqlalchemy.orm import Session
class NodeRepository():
    def __init__(self , session : Session) :
        self.session = session 
    

    def get_all_nodees(self) -> List[NodeDetails]:

        return self.session.execute(select(NodeDetails)).scalars().all()

    def get_node_by_id(self , node_id : str) -> NodeDetails | None:
        return self.session.get(NodeDetails , node_id)