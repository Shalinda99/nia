import json
import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, SYSTEM_PROMPT
from clinical_tools import TOOLS_SCHEMA, execute_tool

logger = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 5
MAX_CONVERSATION_HISTORY = 20


def _get_system_message() -> str:
    now = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
    return f"{SYSTEM_PROMPT}\n\nCurrent date and time: {now}"


class LLMHandler:
    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = LLM_MODEL
        logger.info(f"LLM handler initialized with model: {self.model}")

    async def process(
        self,
        user_text: str,
        conversation_history: List[Dict],
        on_tool_call: Optional[Callable[[str, Dict], None]] = None,
    ) -> str:
        messages = [
            {"role": "system", "content": _get_system_message()},
            *conversation_history[-MAX_CONVERSATION_HISTORY:],
            {"role": "user", "content": user_text},
        ]

        for iteration in range(MAX_TOOL_ITERATIONS):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=TOOLS_SCHEMA,
                    tool_choice="auto",
                    max_tokens=1024,
                    temperature=0.3,
                )
            except Exception as e:
                logger.error(f"LLM API error: {e}")
                return "I'm having trouble connecting to my knowledge system right now. Please check with the charge nurse or consult the paper chart."

            message = response.choices[0].message

            if not message.tool_calls:
                final_text = message.content or "I'm sorry, I didn't understand that. Could you please repeat?"
                return final_text

            messages.append({
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in message.tool_calls
                ],
            })

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                try:
                    tool_args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_args = {}

                if on_tool_call:
                    on_tool_call(tool_name, tool_args)

                tool_result = execute_tool(tool_name, tool_args)
                logger.debug(f"Tool {tool_name} result: {tool_result[:200]}...")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                })

        logger.warning("Max tool iterations reached — returning last assistant message")
        return "I retrieved the information but ran into an issue formatting the response. Please try again."


_llm_handler: Optional[LLMHandler] = None


def get_llm_handler() -> LLMHandler:
    global _llm_handler
    if _llm_handler is None:
        _llm_handler = LLMHandler()
    return _llm_handler
