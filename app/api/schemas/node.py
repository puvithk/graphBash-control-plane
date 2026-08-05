

from sqlalchemy import true
from sqlalchemy import table
from sqlmodel import SQLModel ,Field
from datetime import datetime



class NodeDetails(SQLModel , table=true):
    node_id : str = Field(default=None , primary_key=True)
    
    hostname : str = Field(default=None , index=True)

    node_type : str = Field(default=None , index=True)
    
    node_hostname : str = Field(default=... , description="Node hostname")
    node_ip : str = Field(default=... , description="Node IP")
    node_port : int = Field(default=... , description="Node Port")
    node_os : str = Field(default=... , description="Node OS")
    node_description : str = Field(default=... , description="Node description")
    node_metadata : dict = Field(default=... , description="Node metadata")
    node_status : str = Field(default=... , description="Node status")
    node_created_at : datetime = Field(default=... , description="Node created at")
    node_updated_at : datetime = Field(default=... , description="Node updated at")

    owner_id : str = Field(default=... , description="Owner ID")



    