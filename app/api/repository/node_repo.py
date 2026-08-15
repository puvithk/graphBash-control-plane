from sqlalchemy import select
from app.api.schemas.node import NodeDetails
from typing import List
from sqlalchemy.orm import Session
class NodeRepository():
    def __init__(self , session : Session) :
        self.session = session 
    

    def get_all_nodees(self , owner_id : int) -> List[NodeDetails]:
        return self.session.execute(select(NodeDetails).where(NodeDetails.owner_id == owner_id)).scalars().all()

    def get_node_by_id(self , node_id : str , owner_id : int) -> NodeDetails | None:
        statement = select(NodeDetails).where(
            NodeDetails.node_id ==  node_id  ,
            NodeDetails.owner_id == owner_id
        )
        return self.session.execute(statement).scalar_one_or_none()

    def create_node(self , node: NodeDetails):
        self.session.add(node)
        self.session.commit()
        self.session.refresh(node)

        return node