from langgraph.runtime import Runtime
from src.graph.configuration import Context
from src.graph.agents.base_agent import BaseAgent
from src.config.configs import config_object


class SupervisorAgent(BaseAgent):
    def __init__(self,
                 system_prompt_path: str,
                 runtime: Runtime[Context]):
        super().__init__(system_prompt_path, runtime)

    async def ainvoke(self, state, runtime):
        input_data = {
            "messages": state.messages,
            "memories": state.memories
        }
        if self.agent is None:
            await self.setup_agent(
                url_mcp_servers=config_object.MCP.BASE_MCP_SERVER_URL,
                required_tools=["search_archives", "get_profile_detail"]
            )
        response = await self.agent.ainvoke(input=input_data, runtime=runtime.context, stream=False)
        return response
