# ./src/tools/__init__.py

"""
Public interface for the `tools` package.

Exports:
    - TravelInfo: Tool to get travel currency and exchange information.
    - ToolRouter: Dynamic tool registry and invoker.
    - ToolPayload, ToolCallable,
      ToolFullName, ToolName,
      ToolInstance,Arguments:
        Type hints for working with tools.

Example:
    >>> from tools import TravelInfo, ToolRouter
    >>> travel = TravelInfo("Israel")
    >>> router = ToolRouter()
    >>> router.register_tool_instance("travel_info", travel)
    >>> payload = {
            "tool": "travel_info.get_info",
            "arguments": {
                "country_to": "Japan"
            }
        }
    >>> result = router.call_tool(payload)
    >>> import json
    >>> data = json.loads(result)
    >>> data["country_from"]
    'Israel'
"""

from .travel import TravelInfo
from .tool_router import (
    ToolRouter,
    ToolCallable,
    ToolFullName,
    ToolName,
    ToolPayload,
    Arguments,
    ToolInstance
)

__all__ = [
    "TravelInfo",
    "Arguments",
    "ToolRouter",
    "ToolCallable",
    "ToolFullName",
    "ToolName",
    "ToolPayload",
    "ToolInstance"
]
