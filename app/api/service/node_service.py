

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.dto.node_dto import (
    NodeRegistrationRequestDTO,
    NodeRegistrationToken,
    NodeRegistrationTokenRequest,
    NodeRequestDTO,
)
from app.api.schemas.node import NodeCredential, NodeDetails, NodeRegisterDetails
from app.core.exception import (
    DataBaseException,
    IdRequiredException,
    InvalidTokenException,
    NoOwnerIdProvidedException,
    TokenExpiredException,
    ValueNotFoundException,
)

from ..repository.node_repo import NodeRepository
from ..utils.token import TokenUtils

OWNER_NOT_PRESENT = "Owner not present"


class NodeService:

    def __init__(self , session : Session):
        self.session = session


    def get_all_node(self , owner_id : int | None = None) -> list[NodeDetails]:
        
        node_repo = NodeRepository(self.session)
        if owner_id is None:
            raise NoOwnerIdProvidedException(OWNER_NOT_PRESENT)
        node_list = node_repo.get_all_nodees(owner_id)
        return node_list


    def create_node(self,node_request : NodeRequestDTO , owner_id : int  | None= None) -> NodeDetails:
        
        
        node_repo = NodeRepository(self.session)

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
            node_created_at = datetime.now(tz=UTC),
            node_updated_at = datetime.now(tz=UTC),
            owner_id = owner_id
        )
        
        if owner_id is None:
            raise NoOwnerIdProvidedException(OWNER_NOT_PRESENT)

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
    

    def get_node_by_id(self , node_id : str | None = None , owner_id : int | None = None):
        
        if node_id  is None:
            raise IdRequiredException("Node id is requeired")
        
        if owner_id is None:
            raise NoOwnerIdProvidedException(OWNER_NOT_PRESENT)

        node_repo  = NodeRepository(self.session)

        return node_repo.get_node_by_id(node_id , owner_id)


    def node_registration_request(self , node_request : NodeRegistrationRequestDTO , owner_id : int | None = None) -> NodeRegistrationToken:
        

        # Check weather basic info is present   


        if owner_id is None:
            raise NoOwnerIdProvidedException(OWNER_NOT_PRESENT)


        # Generate a token using secure random module 
        token_utils = TokenUtils()



        try:
            node_repo = NodeRepository(self.session)
            current_node = node_repo.get_node_by_id(node_request.node_id, owner_id)
        except SQLAlchemyError as e:
            raise DataBaseException(str(e)) from e

        if not current_node:
            raise ValueNotFoundException("Node not found")
        
        token_generator =  token_utils.generate_node_registration_token()
        node_registration_token = NodeRegisterDetails(
            token = token_generator,
            node_id = current_node.id ,
            expire_at = datetime.now(tz=UTC) + timedelta(minutes=15),
            created_at = datetime.now(tz=UTC),
            owner_id = owner_id,
        )


        # Create Node Registration Token Update in database
        try:
            node_repo = NodeRepository(self.session)
            node_repo.create_node_registration_token(node_registration_token)
        except SQLAlchemyError as e:
            raise DataBaseException(str(e)) from e        
        # Update the redis Make the expire time currentime + 15 min
        
        
        #Pending  

        # Return the NodeRegistrationToken 
        return {
            "token" : node_registration_token.token,
            "expire_at" : node_registration_token.expire_at,
        }
    
 


    def node_registration(self , node_request : NodeRegistrationTokenRequest):
        """
        This service is used to Node registration with token for the linux system 
        """

        # Check weather the token is present 
        token =  node_request.token 

        if token is None :
            raise ValueNotFoundException("Token is required")

        node_repo = NodeRepository(self.session)
        # Check get the token details from the token 
        try: 
            node_token = node_repo.get_node_registration_token(token)
        except SQLAlchemyError as e:
            raise DataBaseException(str(e)) from e

        if node_token is None:
            raise InvalidTokenException("Invalid Token")
        if node_token.expire_at < datetime.now(tz=UTC):
            raise TokenExpiredException("Token Expired")  
        
        # Generate new API key for the node 
        token_utils = TokenUtils()

        api_key =  token_utils.generate_node_api_key()
        
        api_key_hash = token_utils.generate_node_api_key_has(api_key)

        # Update the node details with the API key and node id
        try: 
            node_repo.create_node_credentials(NodeCredential(
                node_id = node_token.node_id,
                api_key_hash = api_key_hash,
                
            ))
        except SQLAlchemyError as e:
            raise DataBaseException(str(e)) from e  

        # Return the API key and node id

        return {
            "api_key" : api_key,
            "node_id" : str(node_token.node_id)
        }
