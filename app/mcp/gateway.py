

from fastapi import Request
from dotenv.main import logger
from starlette.responses import JSONResponse
class MCPGateway:
    def __init__(self, node_manager):
        self.node_manager = node_manager
    