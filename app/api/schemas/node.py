

from sqlmodel import Relationship
from http.cookiejar import FileCookieJar
from app.api.schemas.user import User
from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import Any
from ast import Dict
from sqlalchemy import true
from sqlalchemy import table
from sqlmodel import SQLModel ,Field
from datetime import datetime



class NodeDetails(SQLModel , table=True):
    node_id : str = Field(default=None , primary_key=True)
    
    hostname : str = Field(default=None , index=True)

    node_type : str = Field(default=None , index=True)

    node_ip : str = Field( description="Node IP")

    node_port : int = Field( description="Node Port")

    node_os : str = Field( description="Node OS")

    node_description : str = Field(description="Node description")

    node_metadata : dict = Field(default={} , sa_column=Column(JSON) , description="Node metadata")

    node_status : str = Field( description="Node status")

    node_created_at : datetime = Field( description="Node created at")

    node_updated_at : datetime = Field( description="Node updated at")

    owner_id : int = Field(
        foreign_key="user.user_id",
        index=True
    )



class NodeCredential(SQLModel , table= True):
    node_id : str = Field(default=None , primary_key=True)

    api_key_hash : str = Field(description="API Key Hash")

    certificate_fingerprint : str = Field(description="Certificate Fingerprint")

    certificate_expiry : datetime = Field(description="Certificate Expiry")

    certificate_serial_number : str = Field(description="Certificate Serial Number")



class NodeLifeCycle(SQLModel , table=True):
    node_id : str = Field(default=None , primary_key=True)

    node_status : str = Field( description="Node status")

    node_updated_at : datetime = Field( description="Node updated at")

    previous_status : str = Field( description="Previous node status")

    reason : str = Field( description="Reason for status change")

    last_connected_at : datetime = Field( description="Last connected at")

    last_disconnected_at : datetime = Field( description="Last disconnected at")

    last_heartbeat : datetime = Field( description="Last heartbeat")

    last_heartbeat_received_at : datetime = Field( description="Last heartbeat received at")

    last_task_sent_at : datetime = Field( description="Last task sent at")

    last_task_received_at : datetime = Field( description="Last task received at")

    

    