from typing import Dict, Any
import json
from .base import AgentState, BaseAgent
from ..memory import ConversationMemory
from ..utils import get_twilio_client


class CallRouterAgent(BaseAgent):
    """Routes incoming calls and manages audio streams"""

    def __init__(self):
        super().__init__("call_router")
        self.memory_store = ConversationMemory()

    async def process(self, state: AgentState) -> AgentState:
        # Load caller memory
        caller_memory = await self.memory_store.get_memory(state.caller_number)
        state.memory.update(caller_memory)

        # Update state with routing decision
        state.current_node = "conversation"
        return state

    async def handle_twilio_stream(self, websocket, openai_ws):
        """Handle bi-directional audio streaming"""
        try:
            while True:
                data = await websocket.receive_text()
                data_json = json.loads(data)

                if data_json["event"] == "start":
                    stream_sid = data_json.get("streamSid")
                    call_sid = data_json.get("start", {}).get("callSid")
                    return stream_sid, call_sid

                elif data_json["event"] == "media" and "payload" in data_json["media"]:
                    payload = data_json["media"]["payload"]
                    # Forward audio to OpenAI
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": payload,
                    }
                    await openai_ws.send(json.dumps(audio_append))

        except Exception as e:
            print(f"Error in stream handling: {e}")
            raise
