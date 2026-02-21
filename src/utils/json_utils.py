# ./src/utils/json_utils.py

import json
import requests
from typing import Any, Dict, Optional, Union

JSONResponse = Union[Dict[str, Any], list[Any]]
"""
Type representing JSON data returned from an API call.

Can be a dictionary or a list of dictionaries/values.
"""


class JSONUtils:
    """
    Utility class for JSON operations, including extraction of
    embedded JSON from text and HTTP GET requests returning JSON.

    Example:
        >>> text = 'Some text {"tool": "travel_info.get_info", "arguments": {"country_to": "Japan"}} more text'
        >>> JSONUtils.extract_json(text, ["tool", "arguments"])
        {'tool': 'travel_info.get_info', 'arguments': {'country_to': 'Japan'}}

        >>> url = "https://restcountries.com/v3.1/name/Israel"
        >>> data = JSONUtils.get_data(url)
        >>> isinstance(data, list)
        True
    """

    @staticmethod
    def extract_json(
        text: str,
        properties: list[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Extract a JSON object from text containing all specified properties.

        Args:
            text (str): Input string possibly containing JSON.
            properties (list[str]): List of required keys the JSON must
                                    contain.

        Returns:
            Optional[Dict[str, Any]]: The first JSON object found containing
                                      all specified properties, or None if
                                      not found.

        Example:
            >>> text = '...{"tool": "travel_info.get_info", "arguments": {"country_to": "Japan"}}...'
            >>> JSONUtils.extract_json(text, ["tool", "arguments"])
            {
                'tool': 'travel_info.get_info',
                'arguments': {'country_to': 'Japan'}
            }
        """
        decoder = json.JSONDecoder()
        idx = 0

        while idx < len(text):
            if text[idx] == "{":
                try:
                    obj, _ = decoder.raw_decode(text[idx:])
                    if isinstance(obj, dict):
                        has_all_required_props = all(
                            prop in obj for prop in properties
                        )
                        if has_all_required_props:
                            return obj
                except json.JSONDecodeError:
                    pass
            idx += 1

        return None

    @staticmethod
    def get_data(
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        """
        Perform an HTTP GET request and return the JSON response.

        Args:
            url (str): URL to request JSON from.
            params (Optional[Dict[str, Any]]): Optional query parameters.

        Returns:
            JSONResponse: Parsed JSON as dict or list.

        Raises:
            requests.HTTPError: If the request fails with a non-2xx status
                                code.

        Example:
            >>> url = "https://restcountries.com/v3.1/name/Israel"
            >>> data = JSONUtils.get_data(url)
            >>> isinstance(data, list)
            True
        """
        response = requests.get(url, timeout=10, params=params)
        response.raise_for_status()
        return response.json()
