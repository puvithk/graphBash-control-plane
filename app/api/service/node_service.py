

from app.core.exception import NoOwnerIdProvidedException
from datetime import datetime
from uuid import uuid4
from app.core.exception import ValueAlreadyExistsException
from app.api.dto.node_dto import NodeRequestDTO
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


    def create_node(self,node_request : NodeRequestDTO) -> NodeDetails:
        
        
        node_repo = NodeRepository(self.session)
        if node_request.node_id:
            if node_repo.get_node_by_id(node_request.node_id):
                raise ValueAlreadyExistsException("Node ID already exisits")

        #generate node id using uuid4
        node_id = uuid4()

        node_details = NodeDetails(
            node_id = node_id,
            hostname = node_request.hostname,
            node_type = node_request.node_type,
            node_ip = node_request.node_ip,
            node_port = node_request.node_port,
            node_os = node_request.node_os,
            node_description = node_request.node_description,
            node_metadata = node_request.node_metadata,
            node_status = node_request.node_status,
            node_created_at = datetime.now(),
            node_updated_at = datetime.now(),
            owner_id = node_request.owner_id
        )
        
        if node_request.owner_id is None:
            raise NoOwnerIdProvidedException("Ownwer not present")

        if node_request.node_status is None:
            node_details.node_status = "Unknown"
        
        if node_request.node_metadata is None:
            node_details.node_metadata = {}
        
        if node_request.node_description is None:
            node_details.node_description = ""
        
        if node_request.node_os is None:
            node_details.node_os = "Unknown"

        if node_request.node_port is None:
            node_details.node_port = 80

        if node_request.node_ip is None:
            node_details.node_ip = "[IP_ADDRESS]"

        if node_request.node_type is None:
            node_details.node_type = "Unknown"

        node_details = node_repo.create_node(node=node_details)
        return node_details
