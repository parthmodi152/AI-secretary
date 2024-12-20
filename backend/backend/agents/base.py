from typing import Dict, Any
from pydantic import BaseModel, Field
from langchain.agents import AgentExecutor
from langgraph.prebuilt import ToolInvocation


class AgentState(BaseModel):
    """Shared state between all agents"""

    call_sid: str
    stream_sid: str | None = None
    caller_number: str
    current_node: str
    messages: list[Dict[str, Any]] = Field(default_factory=list)
    memory: Dict[str, Any] = Field(default_factory=dict)
    tools_output: Dict[str, Any] = Field(default_factory=dict)


class BaseAgent:
    """Base agent class that all other agents inherit from"""

    def __init__(self, name: str):
        self.name = name

    async def process(self, state: AgentState) -> AgentState:
        raise NotImplementedError
