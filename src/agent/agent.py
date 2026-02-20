# ./src/agent/agent.py

import re
import json
from .llm import LLMClient
from .common_data_types import Messages
from utils import JSONUtils
from config import APP_SYSTEM_CONTENT
from tools import ToolRouter, ToolFullName, ToolName, ToolPayload, TravelInfo


TOOL_NAME: ToolName = "travel_info"
TOOL_FULL_NAME: ToolFullName = f"{TOOL_NAME}.get_info"
COUNTRY_FROM = "Israel"
PROPS = ["tool", "arguments"]


class ToolAgent:
    """
    Orchestrates interaction between the LLM and registered tools.

    Responsibilities:
    - Maintain conversation state.
    - Send messages to the LLM.
    - Detect structured tool calls in LLM responses.
    - Execute tools via ToolRouter.
    - Return structured JSON responses.

    Non-responsibilities:
    - Business logic of tools.
    - JSON parsing implementation details.
    - LLM transport-level concerns.

    Example:
        >>> agent = ToolAgent()
        >>> response = agent.run("Can I travel to Japan?")
        >>> isinstance(response, str)
        True
        >>> "error" in response or "result" in response
        True
    """

    def __init__(self) -> None:
        """
        Initialize the agent.

        The constructor:
        - Creates an empty conversation history.
        - Instantiates LLM client and tool router.
        - Adds system-level instruction.
        - Registers default travel tool.

        Example:
            >>> agent = ToolAgent()
            >>> isinstance(agent.messages, list)
            True
        """
        self.messages: Messages = []
        self.llm = LLMClient()
        self.tools = ToolRouter()

        self._add_message("system", APP_SYSTEM_CONTENT)
        self._register_travel_tool(COUNTRY_FROM)

    def _register_travel_tool(self, country_from: str) -> None:
        """
        Register travel information tool with a default origin country.

        Args:
            country_from: Country used as the origin in travel queries.

        Example:
            >>> agent = ToolAgent()
            >>> # Tool is registered during initialization
            >>> isinstance(agent.tools, ToolRouter)
            True
        """
        self.tools.register_tool_instance(
            TOOL_NAME,
            TravelInfo(country_from),
        )

    def _add_message(self, role: str, content: str) -> None:
        """
        Append a message to the conversation history.

        Args:
            role: One of 'system', 'user', 'assistant', 'tool'.
            content: Message text.

        Example:
            >>> agent = ToolAgent()
            >>> agent._add_message("user", "Hello")
            >>> agent.messages[-1]["role"]
            'user'
        """
        self.messages.append({"role": role, "content": content})

    def _get_reply(self) -> str:
        """
        Send conversation history to LLM and return raw reply.

        Returns:
            Raw string returned by the LLM client.

        Note:
            This method assumes LLMClient handles all transport errors.
        """
        return self.llm.send(self.messages)

    def _handle_tool_call(self, tool_data: ToolPayload) -> str:
        """
        Execute tool call extracted from LLM response.

        Flow:
        - Route call via ToolRouter.
        - Normalize tool result to JSON-compatible structure.
        - Append tool message into history.
        - Return serialized JSON result.

        Args:
            tool_data: Parsed JSON containing tool name and arguments.

        Returns:
            JSON string with tool result or error.

        Example (conceptual):
            >>> agent = ToolAgent()
            >>> fake_payload = {
                    "tool": "travel_info.get_info",
                    "arguments": {}
                }
            >>> isinstance(agent._handle_tool_call(fake_payload), str)
            True
        """
        tool_name: ToolFullName = tool_data.get("tool")

        try:
            tool_result = self.tools.call_tool(tool_data)

            # Normalize tool output to dictionary
            if isinstance(tool_result, str):
                try:
                    tool_result = json.loads(tool_result)
                except json.JSONDecodeError:
                    tool_result = {"raw": tool_result}

            content = {"tool": tool_name, "result": tool_result}

            self._add_message("tool", json.dumps(content))
            return json.dumps(tool_result)

        except Exception as e:
            return json.dumps({"error": str(e)})

    def _process_user_message(self) -> str:
        """
        Process latest user message and resolve tool invocation if needed.

        Steps:
        1. Get LLM reply.
        2. Remove markdown code fences if present.
        3. Attempt JSON extraction for tool call.
        4. Execute tool if detected.
        5. Otherwise return structured error.

        Returns:
            JSON string containing result or error.
        """
        reply = self._get_reply()

        # Remove possible ```json or ``` wrappers
        reply = re.sub(r"```json|```", "", reply).strip()

        tool_data = JSONUtils.extract_json(reply, PROPS)

        if tool_data and tool_data.get("tool"):
            return self._handle_tool_call(tool_data)  # type: ignore

        return json.dumps(
            {"error": "Model did not return valid tool call JSON."}
        )

    def run(self, user_input: str) -> str:
        """
        Execute one full interaction cycle.

        Flow:
        - Append user message.
        - Process LLM response.
        - Append assistant response.
        - Return structured JSON result.

        Args:
            user_input: Raw user input string.

        Returns:
            JSON string with tool result or error.

        Example:
            >>> agent = ToolAgent()
            >>> output = agent.run("Is visa required for Japan?")
            >>> isinstance(output, str)
            True
        """
        self._add_message("user", user_input)
        reply = self._process_user_message()
        self._add_message("assistant", reply)
        return reply
