

from typing import Optional
from enum import Enum
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

class NodeStatus(str , Enum):
    PENDING = "pending"
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"
    


class NodeDetails(SQLModel , table=True):

    id : Optional[int] = Field(default=None , primary_key=True)

    node_id : str = Field(default=None , index=True)
    
    hostname : str = Field(default=None )

    node_type : str = Field(default=None)

    node_ip : str = Field( description="Node IP")

    node_port : int = Field( description="Node Port")

    node_os : str = Field( description="Node OS")

    node_description : str = Field(description="Node description")

    node_metadata : dict = Field(default={} , sa_column=Column(JSON) , description="Node metadata")

    node_status : NodeStatus = Field( description="Node status")

    node_created_at : datetime = Field( description="Node created at")

    node_updated_at : datetime = Field( description="Node updated at")

    owner_id : int = Field(
        foreign_key="user.user_id",
        index=True
    )



class NodeCredential(SQLModel , table= True):

    id : Optional[int] = Field(default=None , primary_key=True )

    node_id : int = Field(
        foreign_key="nodedetails.id",
        index= True ,
        description="Node ID" )

    api_key_hash : str = Field(description="API Key Hash")

    certificate_fingerprint : Optional[str] = Field(default=None, description="Certificate Fingerprint" , nullable=True)

    certificate_expiry : Optional[datetime] = Field(default=None, description="Certificate Expiry", nullable=True)

    certificate_serial_number : Optional[str] = Field(default=None, description="Certificate Serial Number", nullable=True)


class NodeRegisterDetails(SQLModel , table=True):

    id : Optional[int] = Field(default=None , primary_key=True )

    node_id : int = Field(
        foreign_key="nodedetails.id",
        index= True , description="Node ID" )

    owner_id : int = Field(
        foreign_key="user.user_id",
        index=True
    )

    token : str = Field(index=True , unique=True , description="Token")

    expire_at : datetime = Field(description="TokenExpire At")

    created_at : datetime = Field(description="Token Created At")






class NodeLifeCycle(SQLModel , table=True):

    id : Optional[int] = Field(default=None , primary_key=True)

    node_id : int = Field(
        foreign_key="nodedetails.id",
        index= True ,
        description="Node ID" )

    node_status : NodeStatus = Field( description="Node status")

    node_updated_at : datetime = Field( description="Node updated at")

    previous_status : Optional[NodeStatus] = Field(default=None, description="Previous node status", nullable=True)

    reason : Optional[str] = Field(default=None, description="Reason for status change", nullable=True)

    last_connected_at : Optional[datetime] = Field(default=None, description="Last connected at", nullable=True)

    last_disconnected_at : Optional[datetime] = Field(default=None, description="Last disconnected at", nullable=True)

    last_heartbeat : Optional[datetime] = Field(default=None, description="Last heartbeat", nullable=True)

    last_heartbeat_received_at : Optional[datetime] = Field(default=None, description="Last heartbeat received at", nullable=True)

    last_task_sent_at : Optional[datetime] = Field(default=None, description="Last task sent at", nullable=True)

    last_task_received_at : Optional[datetime] = Field(default=None, description="Last task received at", nullable=True)

    

    