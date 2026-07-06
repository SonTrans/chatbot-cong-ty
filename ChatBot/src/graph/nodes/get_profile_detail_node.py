from langgraph.runtime import Runtime
from langgraph.types import Command
from langgraph.graph import END

from src.graph.state import State
from src.graph.configuration import Context
from src.graph.agents.get_profile_detail_agent import GetProfileDetailAgent
from src.config.configs import config_prompts

async def get_profile_detail_node(state: State, runtime: Runtime[Context]) -> Command:
    system_prompt_path = config_prompts.PROFILE_GRAPH.PROMPT_GET_PROFILE_DETAIL_PATH
    agent = GetProfileDetailAgent(system_prompt_path, runtime)
    
    response = await agent.ainvoke(state=state, runtime=runtime)
    
    messages = response["messages"]
    ai_message = messages[-1]
    return Command(goto=END, update={"messages": [ai_message]})
