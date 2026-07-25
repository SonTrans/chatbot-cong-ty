import json

from langchain_mcp_adapters.interceptors import MCPToolCallRequest
from mcp.types import CallToolResult, TextContent

async def inject_langgraph_runtime(
    request: MCPToolCallRequest,
    handler,
):
    """
    Interceptor pass-through: forward tool call đến MCP server.
    Không inject thêm field vào args vì các tool MCP (search_archives,
    get_profile_detail) chỉ nhận đúng các parameter đã khai báo trong
    tools.yaml — inject field lạ sẽ gây validation error tại FastMCP.
    """
    result = await handler(request)

    if isinstance(result, CallToolResult) and result.structuredContent is not None:
        return result.model_copy(
            update={
                "content": [
                    TextContent(
                        type="text",
                        text=json.dumps(result.structuredContent, ensure_ascii=False),
                    )
                ]
            }
        )

    return result
