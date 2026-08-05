

from sqlalchemy import true
from sqlalchemy import table
from sqlmodel import SQLModel ,Field
from datetime import datetime



class NodeDetails(SQLModel , table=true):
    node_id : str = Field(default=None , primary_key=True)
    
    hostname : str = Field(default=None , index=True)

    node_type : str = Field(default=None , index=True)

    node_ip : str = Field(default=... , description="Node IP")

    node_port : int = Field(default=... , description="Node Port")

    node_os : str = Field(default=... , description="Node OS")

    node_description : str = Field(default=... , description="Node description")

    node_metadata : dict = Field(default=... , description="Node metadata")

    node_status : str = Field(default=... , description="Node status")

    node_created_at : datetime = Field(default=... , description="Node created at")

    node_updated_at : datetime = Field(default=... , description="Node updated at")

    owner_id : str = Field(default=... , description="Owner ID")

class NodeCredential(SQLModel , table=true):
    node_id : str = Field(default=None , primary_key=True)

    api_key_hash : str = Field(default=... , description="API Key Hash")

    certificate_fingerprint : str = Field(default=... , description="Certificate Fingerprint")

    certificate_expiry : datetime = Field(default=... , description="Certificate Expiry")

    certificate_serial_number : str = Field(default=... , description="Certificate Serial Number")



class NodeLifeCycle(SQLModel , table=true):
    node_id : str = Field(default=None , primary_key=True)

    node_status : str = Field(default=... , description="Node status")

    node_updated_at : datetime = Field(default=... , description="Node updated at")

    previous_status : str = Field(default=... , description="Previous node status")

    reason : str = Field(default=... , description="Reason for status change")

    last_connected_at : datetime = Field(default=... , description="Last connected at")

    last_disconnected_at : datetime = Field(default=... , description="Last disconnected at")

    last_heartbeat : datetime = Field(default=... , description="Last heartbeat")

    last_heartbeat_received_at : datetime = Field(default=... , description="Last heartbeat received at")

    last_task_sent_at : datetime = Field(default=... , description="Last task sent at")

    last_task_received_at : datetime = Field(default=... , description="Last task received at")

    

    