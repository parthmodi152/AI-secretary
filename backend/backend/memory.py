from typing import Dict, Any
import edgedb
from datetime import datetime


class ConversationMemory:
    def __init__(self):
        self.client = edgedb.create_client()

    async def get_memory(self, caller_number: str) -> Dict[str, Any]:
        """Retrieve caller's conversation history"""
        query = """
            SELECT Caller {
                conversations: {
                    timestamp,
                    importance_level,
                    summary,
                    action_taken
                } ORDER BY .timestamp DESC
                LIMIT 5
            }
            FILTER .phone_number = <str>$phone
        """
        result = await self.client.query_single(query, phone=caller_number)

        if not result:
            return {"first_time_caller": True}

        return {
            "first_time_caller": False,
            "conversations": result.conversations,
            "last_interaction": (
                result.conversations[0].timestamp if result.conversations else None
            ),
        }

    async def save_conversation(
        self, caller_number: str, summary: str, importance: str, action_taken: str
    ):
        """Save conversation details"""
        query = """
            WITH
                $caller_number := <str>$phone,
                $summary := <str>$summary,
                $importance := <str>$importance,
                $action := <str>$action
            INSERT Conversation {
                timestamp := datetime_current(),
                importance_level := $importance,
                summary := $summary,
                action_taken := $action,
                caller := (
                    SELECT Caller 
                    FILTER .phone_number = $caller_number
                )
            }
        """
        await self.client.query(
            query,
            phone=caller_number,
            summary=summary,
            importance=importance,
            action=action_taken,
        )
