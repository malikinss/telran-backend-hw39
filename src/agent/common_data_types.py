# ./src/agent/common_data_types.py

from typing import List, Dict, Any

Message = Dict[str, str]
"""
Represents a single chat message exchanged between system,
user, assistant, or tool.

Structure:
    {
        "role": "<role_name>",
        "content": "<text_content>"
    }

Fields:
    role (str):
        Identifies the sender of the message.
        Allowed values (by convention):
            - "system"
            - "user"
            - "assistant"
            - "tool"

    content (str):
        Raw textual content of the message.
        May contain plain text or serialized JSON.

Design Notes:
    - This is intentionally a plain dictionary for simplicity.
    - Avoids coupling to specific LLM provider schemas.
    - Keeps transport format flexible.

Example:
    >>> msg: Message = {"role": "user", "content": "Hello"}
    >>> msg["role"]
    'user'
"""


Messages = List[Message]
"""
Represents the full conversation history exchanged with the LLM.

Ordered list where:
    - Earlier messages appear first.
    - New messages are appended to the end.
    - Order MUST be preserved to maintain conversational context.

Responsibilities:
    - Stores all messages passed to the LLM.
    - Provides contextual memory across requests.

Design Notes:
    - Mutable list is intentional (conversation grows over time).
    - Should only be modified through controlled methods
      (e.g., ToolAgent._add_message).

Example:
    >>> history: Messages = []
    >>> history.append({"role": "system", "content": "You are helpful."})
    >>> len(history)
    1
"""


Payload = Dict[str, Any]
"""
Generic structured data container.

Used for:
    - Tool invocation payloads
    - API request bodies
    - Parsed JSON data
    - Arbitrary structured data exchange

Unlike Message:
    - Values are not restricted to strings.
    - Can contain nested dictionaries and lists.

Design Notes:
    - Flexible but unvalidated.
    - Higher-level logic should validate expected keys.

Example:
    >>> payload: Payload = {
            "tool": "travel_info.get_info",
            "arguments": {"country": "Japan"}
        }
    >>> "arguments" in payload
    True
"""
