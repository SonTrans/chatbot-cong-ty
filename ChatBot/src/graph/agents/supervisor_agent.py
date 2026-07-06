from enum import Enum
from langgraph.runtime import Runtime
from langgraph.types import Command
from pydantic import BaseModel, Field

from src.graph.configuration import Context
from src.graph.agents.base_agent import BaseAgent
from src.log import logger

class AgentEnum(str, Enum):
    SEARCH_PROFILE = {"value": "SEARCH_PROFILE", "description": "Agent tìm kiếm hồ sơ. Sử dụng khi người dùng cung cấp từ khóa, tên, chức vụ hoặc một số thông tin nhưng chưa có mã archive_id."}
    GET_PROFILE_DETAIL = {"value": "GET_PROFILE_DETAIL", "description": "Agent tra cứu chi tiết hồ sơ. Sử dụng BẮT BUỘC khi bạn đã biết archive_id và muốn xem bên trong hồ sơ đó có gì."}

    def __new__(cls, obj):
        value = obj["value"]
        description = obj["description"]
        instance = str.__new__(cls, value)
        instance._value_ = value
        instance.description = description
        return instance

def build_enum_description(enum_cls):
    return "\n".join(f"- `{e.value}`: {e.description}" for e in enum_cls)

class SupervisorAgentResponse(BaseModel):
    worker: AgentEnum = Field(
        description=f"Xác định agent thực hiện nhiệm vụ tiếp theo. Hãy đọc kĩ cuộc hội thoại, chọn 1 trong {len(AgentEnum)} agents sau: \n" + build_enum_description(AgentEnum),
        examples=[e.value for e in AgentEnum])

class SupervisorAgent(BaseAgent):
    def __init__(self, system_prompt_path: str, runtime: Runtime[Context]):
        super().__init__(system_prompt_path, runtime)

    async def ainvoke(self, state, runtime):
        input_data = {
            "messages": state.messages
        }
        await self.setup_agent(response_class=SupervisorAgentResponse, use_only_response_structured=True)
        response = await self.agent.ainvoke(input=input_data, runtime=runtime.context)
        structured_response = response["structured_response"]
        worker = structured_response.worker.value
        logger.info(f"---SUPERVISOR -> {worker}---")
        return Command(goto=worker)
