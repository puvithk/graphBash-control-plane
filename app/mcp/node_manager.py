
from pydantic import BaseModel , field_validator
from .schemas import NodeRegistration
from pydantic import ConfigDict
class NodeManager(BaseModel):

    model_config = ConfigDict(extra="ignore")

    _nodes : dict[str, NodeRegistration]

    @field_validator("_nodes")
    @classmethod
    def validate__nodes(cls , value: dict[str, NodeRegistration]):
        return value

    def register_node(self , node_registration : NodeRegistration):
        if self._nodes.get(node_registration.node_id) is not None:
            raise ValueError(f"Node {node_registration.node_id} already registered")
        
        self._nodes[node_registration.node_id] = node_registration


    def get_tools(self , node_id : str) -> list[NodeRegistration]:

        node = self._nodes.get(node_id , None)
        if node is None:
            raise ValueError(f"Node {node_id} not registered")

        return node.node_tools

    
