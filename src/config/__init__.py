# ./src/config/__init__.py

"""
Public interface for the `config` module.

Provides predefined system instructions for Phi-3 travel assistant LLM.

Design goals:
    - Centralize system prompts.
    - Expose only stable constants as public API.
    - Enable easy import from other modules.

Example:
    >>> from config import APP_SYSTEM_CONTENT, INNER_SYSTEM_CONTENT
    >>> "travel assistant" in APP_SYSTEM_CONTENT
    True
"""

from .system_content import APP_SYSTEM_CONTENT, INNER_SYSTEM_CONTENT

__all__ = [
    "APP_SYSTEM_CONTENT",
    "INNER_SYSTEM_CONTENT",
]
