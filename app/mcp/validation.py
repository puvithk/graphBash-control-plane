
from pydantic import BaseModel
from .schemas import ToolRequest
from .node_manager import NodeManager
from .registry import ToolRegistry


class RequestValidator():
    def __init__(
        self,
        registry: ToolRegistry,
        node_manager: NodeManager,
    ) -> None:
        self.registry = registry
        self.node_manager = node_manager

    def validate(self, request: ToolRequest) -> None:
        self.registry.get(request.tool_name)

        node = self.node_manager.get(request.node_id)

        if request.tool_name not in node.node_tools:
            raise ValueError(
                "Node does not support this tool"
            )

        if request.arguments:
            raise ValueError(
                "System tools do not accept arguments"
            )