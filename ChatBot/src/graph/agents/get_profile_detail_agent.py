from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.runtime import Runtime

from src.graph.configuration import Context
from src.graph.agents.base_agent import BaseAgent
from src.config.configs import config_object
from src.graph.middlewares.simple_middlewares import inject_config_prompt
from src.log import logger


class GetProfileDetailAgent(BaseAgent):
    def __init__(self, system_prompt_path: str, runtime: Runtime[Context]):
        super().__init__(system_prompt_path, runtime)

    async def ainvoke(self, state, runtime):
        input_data = {
            "messages": state.messages,
            "memories": state.memories
        }

        url = config_object.MCP.BASE_MCP_SERVER_URL
        transport = config_object.MCP.BASE_MCP_SERVER_TRANSPORT

        # Dùng client.session() context manager để giữ MCP session SỐNG
        # trong suốt quá trình agent gọi tool
        mcp_client = MultiServerMCPClient(
            {
                "MCP Server": {
                    "url": url,
                    "transport": transport,
                    "timeout": 120,
                    "sse_read_timeout": 120,
                }
            }
        )

        async with mcp_client.session("MCP Server") as session:
            tools_all = await load_mcp_tools(session)
            tools = [t for t in tools_all if t.name == "get_profile_detail"]
            logger.info(f"[GetProfileDetailAgent] Loaded tools: {[t.name for t in tools]}")

            agent = create_agent(
                self.model,
                tools=tools,
                system_prompt=self.system_prompt,
                middleware=[inject_config_prompt],
            )
            response = await agent.ainvoke(input=input_data, runtime=runtime.context)

        return response
