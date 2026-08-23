

from app.api.schemas.node import NodeStatus
from pydantic import BaseModel , Field
from datetime import datetime
class NodeRequestDTO(BaseModel):



    hostname : str = Field(default=None , index=True)

    node_type : str = Field(default=None , index=True)

    node_ip : str = Field( description="Node IP")

    node_port : int = Field( description="Node Port")

    node_os : str = Field( description="Node OS")

    node_description : str = Field(description="Node description")

    node_metadata : dict = Field(default=None , index=True)

    node_status : NodeStatus = Field(default=None , index=True)

class NodeRegistrationRequestDTO(BaseModel):
    node_id : str = Field(description="Node ID")





    
    
class NodeRegistrationToken(BaseModel):

    token : str = Field(description="Token")

    expire_at : datetime = Field(description="TokenExpire At")

class NodeRegistrationResponse(BaseModel):

    api_key : str = Field(description="API KEY for the node")

    node_id : str = Field(description="Node ID")


    # Should add CA certifiacates In next phase 
    

class NodeRegistrationTokenRequest(BaseModel):

    token : str = Field(description="Token")



