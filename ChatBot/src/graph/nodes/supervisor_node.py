from langgraph.runtime import Runtime
from langgraph.types import Command

from src.graph.state import State
from src.graph.configuration import Context
from src.graph.agents.supervisor_agent import SupervisorAgent
from src.config.configs import config_prompts

async def supervisor_node(state: State, runtime: Runtime[Context]) -> Command:
    system_prompt_path = config_prompts.PROFILE_GRAPH.PROMPT_SUPERVISOR_PATH
    agent = SupervisorAgent(system_prompt_path, runtime)
    command_goto = await agent.ainvoke(state=state, runtime=runtime)
    return command_goto
