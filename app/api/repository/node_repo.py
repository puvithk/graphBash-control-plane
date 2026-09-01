from app.api.schemas.node import NodeCredential
from app.api.schemas.node import NodeRegisterDetails
from app.api.dto.node_dto import NodeRegistrationToken
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


    def create_node_registration_token(self , node_registration_token : NodeRegisterDetails):
        # Add to the session 
        self.session.add(node_registration_token)
        # commit the session 
        self.session.commit()
        self.session.refresh(node_registration_token)

        return node_registration_token


    def get_node_registration_token(self , token : str) -> NodeRegisterDetails | None:
        statement = select(NodeRegisterDetails).where(
            NodeRegisterDetails.token ==  token  ,
        )
        return self.session.execute(statement).scalar_one_or_none()

    def delete_node_registration_token(self , token : str , owner_id : int):
        self.session.execute(select(NodeRegisterDetails).where(
            NodeRegisterDetails.token ==  token  ,
            NodeRegisterDetails.owner_id == owner_id
        ))
        self.session.commit()

    def create_node_credentials(self , node_credentials : NodeCredential):
        self.session.add(node_credentials)
        self.session.commit()
        self.session.refresh(node_credentials)
        return node_credentials