from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.runtime import Runtime

from src.graph.configuration import Context
from src.graph.agents.base_agent import BaseAgent
from src.config.configs import config_object
from src.graph.middlewares.simple_middlewares import inject_config_prompt
from src.log import logger


class SearchProfileAgent(BaseAgent):
    def __init__(self, system_prompt_path: str, runtime: Runtime[Context]):
        super().__init__(system_prompt_path, runtime)

    async def ainvoke(self, state, runtime):
        input_data = {
            "messages": state.messages,
            "memories": state.memories
        }

        url = config_object.MCP.BASE_MCP_SERVER_URL
        transport = config_object.MCP.BASE_MCP_SERVER_TRANSPORT

        mcp_client = MultiServerMCPClient(
            {
                "MCP Server": {
                    "url": url,
                    "transport": transport,
                    "timeout": 120,
                    "sse_read_timeout": 120,
                    # Truyền read_timeout_seconds cho ClientSession
                    # để session.call_tool() chờ đủ lâu
                    "session_kwargs": {
                        "read_timeout_seconds": __import__("datetime").timedelta(seconds=120)
                    }
                }
            }
        )

        async with mcp_client.session("MCP Server") as session:
            tools_all = await load_mcp_tools(session)
            tools = [t for t in tools_all if t.name == "search_profile"]
            logger.info(f"[SearchProfileAgent] Tools loaded: {[t.name for t in tools]}")

            agent = create_agent(
                self.model,
                tools=tools,
                system_prompt=self.system_prompt,
                middleware=[inject_config_prompt],
            )
            response = await agent.ainvoke(input=input_data, runtime=runtime.context)

        # Log messages để debug
        messages = response.get("messages", [])
        for msg in messages:
            msg_type = type(msg).__name__
            content_preview = str(msg.content)[:200] if msg.content else "(empty)"
            logger.info(f"[SearchProfileAgent] {msg_type}: {content_preview}")

        return response
