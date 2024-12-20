from fastapi import FastAPI, WebSocket
from langgraph.graph import Graph
import asyncio
import json
import websockets
from .agents.base import AgentState
from .agents.call_router import CallRouterAgent
from .agents.conversation import ConversationAgent
from .agents.action import ActionAgent
from .utils import get_twilio_client
import os

app = FastAPI()

# Initialize agents
call_router = CallRouterAgent()
conversation = ConversationAgent()
action = ActionAgent()


# Build graph
def build_graph():
    graph = Graph()

    # Add nodes
    graph.add_node("call_router", call_router.process)
    graph.add_node("conversation", conversation.process)
    graph.add_node("action", action.process)

    # Add edges
    graph.add_edge("call_router", "conversation")
    graph.add_edge("conversation", "action")
    graph.add_edge("action", "end")

    return graph


workflow = build_graph()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Initialize OpenAI Realtime connection
    async with websockets.connect(
        "wss://api.openai.com/v1/realtime",
        extra_headers={
            "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
            "OpenAI-Beta": "realtime=v1",
        },
    ) as openai_ws:
        # Initialize call router
        stream_sid, call_sid = await call_router.handle_twilio_stream(
            websocket, openai_ws
        )

        # Initialize state
        state = AgentState(
            call_sid=call_sid,
            stream_sid=stream_sid,
            caller_number=await get_caller_number(call_sid),
            current_node="call_router",
        )

        # Start graph execution
        config = workflow.compile()
        for output in config.run(state):
            # Handle state updates
            print(f"Current node: {output.current_node}")
