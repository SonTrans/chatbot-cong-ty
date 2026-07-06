import traceback
from langgraph.runtime import Runtime
from langgraph.types import Command
from langgraph.graph import END

from src.graph.state import State
from src.graph.configuration import Context
from src.graph.agents.search_profile_agent import SearchProfileAgent
from src.config.configs import config_prompts
from src.log import logger

async def search_profile_node(state: State, runtime: Runtime[Context]) -> Command:
    system_prompt_path = config_prompts.PROFILE_GRAPH.PROMPT_SEARCH_PROFILE_PATH
    agent = SearchProfileAgent(system_prompt_path, runtime)
    
    try:
        response = await agent.ainvoke(state=state, runtime=runtime)
        messages = response["messages"]
        ai_message = messages[-1]
        return Command(goto=END, update={"messages": [ai_message]})
    except Exception as e:
        logger.error(f"[SEARCH_PROFILE_NODE] Exception: {type(e).__name__}: {e}")
        logger.error(traceback.format_exc())
        raise
