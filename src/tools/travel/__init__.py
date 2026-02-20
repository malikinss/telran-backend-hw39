# ./src/tools/travel/__init__.py

"""
Public interface for the `tools.travel` package.

Exports:
    - TravelInfo: Tool to get travel currency and exchange information.
    - TravelResult: TypedDict describing the structure of the returned data.

Example:
    >>> from tools.travel import TravelInfo, TravelResult
    >>> travel = TravelInfo("Israel")
    >>> json_str = travel.get_info("Japan")
    >>> import json
    >>> data: TravelResult = json.loads(json_str)
    >>> data["country_from"]
    'Israel'
    >>> "JPY" in data["code_to"]
    True
"""

from .travel_info import TravelInfo, TravelResult

__all__ = ["TravelInfo", "TravelResult"]
