

from app.core.exception import ValueNotFoundException
from app.api.schemas.node import NodeRegisterDetails
from app.core.exception import DataBaseException
from app.api.dto.node_dto import NodeRegistrationToken
from app.core.exception import IdRequiredException
from app.core.exception import NoOwnerIdProvidedException
from datetime import datetime , timedelta
from uuid import uuid4
from app.core.exception import ValueAlreadyExistsException , ValueRequiredException
from app.api.dto.node_dto import NodeRequestDTO
from app.api.schemas.node import NodeDetails
from typing import List
from sqlalchemy.orm import Session
from ..repository.node_repo import NodeRepository
from ..utils.token import TokenUtils
class NodeService():

    def __init__(self , session : Session):
        self.session = session


    def get_all_node(self , owner_id : int) -> List[NodeDetails]:
        
        node_repo = NodeRepository(self.session)
        if owner_id is None:
            raise NoOwnerIdProvidedException("Owner not present")
        node_list = node_repo.get_all_nodees(owner_id)
        return node_list


    def create_node(self,node_request : NodeRequestDTO , owner_id : int = None) -> NodeDetails:
        
        
        node_repo = NodeRepository(self.session)

        if node_request.node_id:
            if node_repo.get_node_by_id(node_request.node_id , owner_id):
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
            owner_id = owner_id
        )
        
        if owner_id is None:
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
    

    def get_node_by_id(self , node_id : str = None , owner_id : int = None):
        
        if node_id  is None:
            raise IdRequiredException("Node id is requeired")
        
        if owner_id is None:
            raise NoOwnerIdProvidedException("Owner not present")

        node_repo  = NodeRepository(self.session)

        return node_repo.get_node_by_id(node_id , owner_id)


    def node_registration_request(self , node_request : NodeRequestDTO , owner_id : int = None) -> NodeRegistrationToken:
        

        # Check weather basic info is present   


        if owner_id is None:
            raise NoOwnerIdProvidedException("Owner not present")


        # Generate a token using secure random module 
        token_utils = TokenUtils()



        try :
            node_repo = NodeRepository(self.session)
            current_node = node_repo.get_node_by_id(node_request.node_id , owner_id)
            if not current_node:
                raise ValueNotFoundException("Node not found")
        except ValueNotFoundException as ve :
            raise ve
        except Exception as e:
            raise DataBaseException(str(e))
        
        token_generator =  token_utils.generate_node_registration_token()
        node_registration_token = NodeRegisterDetails(
            token = token_generator,
            node_id = current_node.id ,
            expire_at = datetime.now() + timedelta(minutes=15),
            created_at = datetime.now(),
            owner_id = owner_id,
        )


        # Create Node Registration Token Update in database
        try :
            node_repo = NodeRepository(self.session)
            node_repo.create_node_registration_token(node_registration_token)
        except Exception as e :
            raise DataBaseException(str(e))        
        # Update the redis Make the expire time currentime + 15 min
        
        
        #Pending  

        # Return the NodeRegistrationToken 
        return {
            "token" : node_registration_token.token,
            "expire_at" : node_registration_token.expire_at,
        }
    
 


