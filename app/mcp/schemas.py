from typing import Any
from pydantic import BaseModel , Field ,  ConfigDict


class ToolMetadata(BaseModel):

    model_config = ConfigDict(extra="forbid")

    name : str = Field(default=... , description="Tool name")
    description : str = Field(default=... , description="Tool description")
    input_schema : dict = Field(default=... , description="Tool input schema")
    output_schema : dict = Field(default=... , description="Tool output schema")


class NodeRegistation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    node_id : str = Field(default=... , description="Node ID")
    node_name : str = Field(default=... , description="Node name")
    node_type : str = Field(default=... , description="Node type")
    node_hostname : str = Field(default=... , description="Node hostname")
    node_ip : str = Field(default=... , description="Node IP")
    node_port : int = Field(default=... , description="Node Port")
    node_os : str = Field(default=... , description="Node OS")
    node_description : str = Field(default=... , description="Node description")
    node_metadata : dict = Field(default=... , description="Node metadata")
    node_tools : list[ToolMetadata] = Field(default=... , description="List of node tools")

class ToolRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    node_id : str = Field(default=... , description="Node ID")
    tool_name : str = Field(default=... , description="Tool name")
    tool_input : dict[str , Any] = Field(default=... , description="Tool input")