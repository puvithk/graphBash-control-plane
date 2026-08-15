

from app.api.schemas.node import NodeStatus
from pydantic import BaseModel , Field
from datetime import datetime
class NodeRequestDTO(BaseModel):

    node_id : str = Field(default=None)
    
    hostname : str = Field(default=None)

    node_type : str = Field(default=None)

    node_ip : str = Field( description="Node IP")

    node_port : int = Field( description="Node Port")

    node_os : str = Field( description="Node OS")

    node_description : str = Field(description="Node description")

    node_metadata : dict = Field(default={} , description="Node metadata")

    node_status : NodeStatus = Field( description="Node status")

