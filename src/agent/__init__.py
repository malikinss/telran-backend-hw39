# ./src/agent/__init__.py

"""
Public package interface for the `agent` module.

This file defines the stable, supported API surface of the package.
External consumers should import from `agent` directly instead of
accessing internal modules.

Design Goals:
    - Provide a clean entrypoint for consumers.
    - Hide internal structure.
    - Control what is considered public API.

Example:
    >>> from agent import ToolAgent
    >>> agent = ToolAgent()
    >>> isinstance(agent, ToolAgent)
    True

    >>> from agent import AgentCLI
    >>> cli = AgentCLI()
    >>> hasattr(cli, "run")
    True
"""
from .cli import AgentCLI
from .llm import LLMClient
from .agent import ToolAgent
from .common_data_types import Message, Messages, Payload

__all__ = [
    "AgentCLI",
    "LLMClient",
    "ToolAgent",
    "Message",
    "Messages",
    "Payload"
]
