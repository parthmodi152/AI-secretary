from typing import Dict, Any
from .base import AgentState, BaseAgent
from ..utils import transfer_call, schedule_call, end_call
from ..memory import ConversationMemory


class ActionAgent(BaseAgent):
    """Executes actions based on conversation decisions"""

    def __init__(self):
        super().__init__("action")
        self.memory_store = ConversationMemory()

    async def process(self, state: AgentState) -> AgentState:
        # Get the function call from OpenAI
        function_name = state.tools_output.get("name")

        if function_name == "transfer_call":
            await transfer_call(state.call_sid)
            action = "transferred"

        elif function_name == "schedule_call":
            await schedule_call(state.caller_number)
            action = "scheduled"

        elif function_name == "hang_up":
            await end_call(state.call_sid)
            action = "hung_up"

        # Save conversation to memory
        await self.memory_store.save_conversation(
            caller_number=state.caller_number,
            summary=state.messages[-1]["content"],  # Last message
            importance=self._determine_importance(function_name),
            action_taken=action,
        )

        state.current_node = "end"
        return state

    def _determine_importance(self, action: str) -> str:
        if action == "transfer_call":
            return "very"
        elif action == "schedule_call":
            return "some"
        return "none"
