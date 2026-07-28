from pydantic import BaseModel
from .schemas import ToolMetadata

class ToolRegistry(BaseModel):

    def __init__(self):
        self._tools :  dict[str , ToolMetadata]
    

    def register(self , tool_metadata : ToolMetadata):

        if self._tools.get(tool_metadata.name) is not None :
            raise ValueError(f"Tool {tool_metadata.name} already registered")
        
        self._tools[tool_metadata.name] = tool_metadata

    def get_tools(self , tool_name : str):
        tool = self._tools.get(tool_name)

        if tool is None :
            raise ValueError(f"Tool {tool_name} is not registered")
        
        return tool
    
    def list_tools(self):
        return self._tools.keys()
    