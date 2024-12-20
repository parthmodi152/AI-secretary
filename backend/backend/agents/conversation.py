from typing import Dict, Any
import json
from .base import AgentState, BaseAgent
from ..google_functions import get_events_for_today


class ConversationAgent(BaseAgent):
    """Handles the main conversation logic with Donna's personality"""

    def __init__(self):
        super().__init__("conversation")

    def _build_system_prompt(self, state: AgentState) -> str:
        # Get calendar info
        calendar_info = get_events_for_today()

        # Build context from memory
        memory_context = ""
        if not state.memory.get("first_time_caller"):
            conversations = state.memory.get("conversations", [])
            if conversations:
                last_interaction = conversations[0]
                memory_context = f"""
                Previous interaction: {last_interaction['summary']}
                Last importance level: {last_interaction['importance_level']}
                Last action taken: {last_interaction['action_taken']}
                """

        return f"""You are Donna, a personal assistant with the personality of Donna from Suits.
        {memory_context}
        Current calendar: {calendar_info}
        
        Available actions:
        - transfer_call: For very important calls
        - schedule_call: For non-urgent matters
        - hang_up: For spam or unnecessary calls
        
        Remember: Be witty, confident, and protective of Harvey's time."""

    async def process(self, state: AgentState) -> AgentState:
        # Initialize OpenAI session with system prompt
        session_update = {
            "type": "session.update",
            "session": {
                "turn_detection": {"type": "server_vad"},
                "input_audio_format": "g711_ulaw",
                "output_audio_format": "g711_ulaw",
                "voice": "alloy",
                "instructions": self._build_system_prompt(state),
                "tools": [
                    {
                        "type": "function",
                        "name": "transfer_call",
                        "description": "Transfer call to Harvey",
                    },
                    {
                        "type": "function",
                        "name": "schedule_call",
                        "description": "Send scheduling link",
                    },
                    {
                        "type": "function",
                        "name": "hang_up",
                        "description": "End the call",
                    },
                ],
            },
        }

        # Update state
        state.current_node = "action"
        return state
