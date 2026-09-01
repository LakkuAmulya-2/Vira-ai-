from app.mcp.contracts import MCPToolRequest, MCPToolResponse


class MCPGateway:
    def __init__(self, allowed_servers: set[str]) -> None:
        self.allowed_servers = allowed_servers

    async def call(self, request: MCPToolRequest) -> MCPToolResponse:
        if request.server not in self.allowed_servers:
            raise PermissionError(f"MCP server is not allowlisted: {request.server}")
        raise NotImplementedError(
            "Transport adapters must be registered per approved MCP server."
        )
