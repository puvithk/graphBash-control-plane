


from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class NodeStatus(str , Enum):
    PENDING = "pending"
    REGISTERED = "registered"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"
    
NODE_DETAILS = "nodedetails"
NODE_DESCRIPTION = "Node ID"

class NodeDetails(SQLModel , table=True):

    __tablename__ = NODE_DETAILS

    id : int | None = Field(default=None , primary_key=True)

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

    id : int | None = Field(default=None , primary_key=True )

    node_id : int = Field(
        foreign_key=f"{NODE_DETAILS}.id",
        index= True ,
        description=NODE_DESCRIPTION     )

    api_key_hash : str = Field(description="API Key Hash")

    certificate_fingerprint : str | None = Field(default=None, description="Certificate Fingerprint" , nullable=True)

    certificate_expiry : datetime | None = Field(default=None, description="Certificate Expiry", nullable=True)

    certificate_serial_number : str | None = Field(default=None, description="Certificate Serial Number", nullable=True)


class NodeRegisterDetails(SQLModel , table=True):

    id : int | None = Field(default=None , primary_key=True )

    node_id : int = Field(
        foreign_key=f"{NODE_DETAILS}.id",
        index= True , description=NODE_DESCRIPTION )

    owner_id : int = Field(
        foreign_key="user.user_id",
        index=True
    )

    token : str = Field(index=True , unique=True , description="Token")

    expire_at : datetime = Field(description="TokenExpire At")

    created_at : datetime = Field(description="Token Created At")






class NodeLifeCycle(SQLModel , table=True):

    id : int | None = Field(default=None , primary_key=True)

    node_id : int = Field(
        foreign_key=f"{NODE_DETAILS}.id",
        index= True ,
        description=NODE_DESCRIPTION )

    node_status : NodeStatus = Field( description="Node status")

    node_updated_at : datetime = Field( description="Node updated at")

    previous_status : NodeStatus | None = Field(default=None, description="Previous node status", nullable=True)

    reason : str | None = Field(default=None, description="Reason for status change", nullable=True)

    last_connected_at : datetime | None = Field(default=None, description="Last connected at", nullable=True)

    last_disconnected_at : datetime | None = Field(default=None, description="Last disconnected at", nullable=True)

    last_heartbeat : datetime | None = Field(default=None, description="Last heartbeat", nullable=True)

    last_heartbeat_received_at : datetime | None = Field(default=None, description="Last heartbeat received at", nullable=True)

    last_task_sent_at : datetime | None = Field(default=None, description="Last task sent at", nullable=True)

    last_task_received_at : datetime | None = Field(default=None, description="Last task received at", nullable=True)

    

    