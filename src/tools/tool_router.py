# ./src/tools/tool_router.py

from typing import Dict, Any, TypedDict, Callable

# Type aliases for tool routing
ToolName = str
ToolFullName = str
ToolInstance = object
Arguments = Dict[str, Any]
ToolCallable = Callable[..., Any]


class ToolPayload(TypedDict):
    """
    Structured payload representing a tool call request.

    Fields:
        tool (str): Full tool name (e.g., "travel_info.get_info").
        arguments (dict): Keyword arguments for the tool call.

    Example:
        >>> payload: ToolPayload = {
        ...     "tool": "travel_info.get_info",
        ...     "arguments": {"country_to": "Japan"}
        ... }
    """
    tool: ToolFullName
    arguments: Dict[str, Any]


class ToolRouter:
    """
    Registry and invoker for tool instances and their callable methods.

    Responsibilities:
        - Register tool instances.
        - Map tool methods to fully-qualified names.
        - Invoke tools dynamically given a ToolPayload.

    Example:
        >>> from tools.travel import TravelInfo
        >>> router = ToolRouter()
        >>> router.register_tool_instance("travel_info", TravelInfo("Israel"))
        >>> payload = {
                "tool": "travel_info.get_info",
                "arguments": {
                    "country_to": "Japan"
                }
            }
        >>> result = router.call_tool(payload)
        >>> isinstance(result, str)
        True
    """

    def __init__(self) -> None:
        """
        Initialize empty tool registry.
        """
        self._tool_instances: Dict[ToolName, ToolInstance] = {}
        self._tool_methods: Dict[ToolFullName, ToolCallable] = {}

    def register_tool_instance(
        self, name: ToolName, instance: ToolInstance
    ) -> None:
        """
        Register a tool instance and map all its public callables.

        Args:
            name (str): Tool base name.
            instance (object): Tool instance object.

        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if name in self._tool_instances:
            raise ValueError(f"Tool instance already registered: {name}")

        self._tool_instances[name] = instance
        for attr_name in dir(instance):
            if attr_name.startswith("_"):
                continue
            attr = getattr(instance, attr_name)
            if callable(attr):
                tool_key: ToolFullName = f"{name}.{attr_name}"
                self._tool_methods[tool_key] = attr

    def get_tool(self, name: ToolFullName) -> ToolCallable:
        """
        Retrieve a tool method by its fully-qualified name.

        Args:
            name (str): Full tool name (e.g., "travel_info.get_info").

        Returns:
            Callable: The method associated with the tool.

        Raises:
            ValueError: If tool is not registered.
        """
        tool = self._tool_methods.get(name)
        if tool is None:
            raise ValueError(f"Unknown tool: {name}")
        return tool

    def call_tool(self, tool_data: ToolPayload) -> Any:
        """
        Dynamically call a tool given a payload.

        Args:
            tool_data (ToolPayload): Dictionary containing 'tool' and
                                     'arguments' keys.

        Returns:
            Any: Result returned by the tool callable.

        Raises:
            ValueError: If tool name is missing or unknown.
        """
        tool_name: ToolFullName = tool_data["tool"]
        arguments: Arguments = tool_data["arguments"]

        if not tool_name:
            raise ValueError("Tool name is empty.")

        # Shortcut for default travel_info method
        if "." not in tool_name and tool_name == "travel_info":
            tool_name = f"{tool_name}.get_info"

        tool: ToolCallable = self.get_tool(tool_name)
        return tool(**arguments)
