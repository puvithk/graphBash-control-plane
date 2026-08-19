

from app.api.schemas.node import NodeStatus
from pydantic import BaseModel , Field
from datetime import datetime
class NodeRequestDTO(BaseModel):

    node_id : str = Field(default=None)
    
    
class NodeRegistrationToken(BaseModel):

    token : str = Field(description="Token")

    expire_at : datetime = Field(description="TokenExpire At")



    