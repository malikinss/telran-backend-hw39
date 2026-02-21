# ./src/utils/__init__.py

"""
Utility package exposing commonly used helper classes.

This module aggregates and re-exports core utility components
to provide a clean and convenient public API for the `utils` package.

Exports:
    ThinkingDots: Console-based animated progress indicator.
    JSONUtils: Utility helpers for safe JSON parsing and validation.
    CurrencyUtils: Currency-related helper functions.
    CurrencyInfo: Data structure representing currency metadata.

Example:
    >>> from src.utils import ThinkingDots, JSONUtils
    >>> dots = ThinkingDots("Loading")
    >>> dots.start()
    >>> dots.stop()
"""
from .json_utils import JSONUtils
from .thinking_dots import ThinkingDots
from .currency_utils import CurrencyUtils, CurrencyInfo


__all__ = [
    "JSONUtils",
    "ThinkingDots",
    "CurrencyInfo",
    "CurrencyUtils",
]
