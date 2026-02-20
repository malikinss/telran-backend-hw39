# ./src/tools/travel/travel_info.py

import json
from typing import Optional, TypedDict
from utils import CurrencyUtils


class TravelResult(TypedDict):
    """
    Structured result of a travel currency query.

    Fields:
        country_from (str): Origin country name.
        country_to (str): Destination country name.
        code_from (str): Currency code of origin country.
        code_to (str): Currency code of destination country.
        currency_name (str): Name of the destination currency.
        exchange_rate (float): Conversion rate from origin to destination
                               currency.

    Example:
        >>> result: TravelResult = {
        ...     "country_from": "Israel",
        ...     "country_to": "Japan",
        ...     "code_from": "ILS",
        ...     "code_to": "JPY",
        ...     "currency_name": "Yen",
        ...     "exchange_rate": 40.5
        ... }
    """
    country_from: str
    country_to: str
    code_from: str
    code_to: str
    currency_name: str
    exchange_rate: float


class TravelInfo:
    """
    Tool to provide travel currency information and exchange rates.

    Initialized with a country of origin and can provide data for
    any destination country.

    Example:
        >>> travel = TravelInfo("Israel")
        >>> travel.get_info("Japan")  # returns JSON string with TravelResult
    """

    def __init__(self, country_from: str) -> None:
        """
        Initialize the tool with the origin country.

        Args:
            country_from (str): Name of the country of origin.
        """
        self.country_from: str = country_from
        self._code_from: Optional[str] = None

    @property
    def code_from(self) -> str:
        """
        Lazy-loaded currency code of the origin country.

        Returns:
            str: ISO currency code (e.g., 'ILS').

        Example:
            >>> travel = TravelInfo("Israel")
            >>> travel.code_from
            'ILS'
        """
        if self._code_from is None:
            currency = CurrencyUtils.get_country_currency(self.country_from)
            self._code_from = currency["currency_code"]

        return self._code_from

    def get_info(self, country_to: str) -> str:
        """
        Return travel currency information and exchange rate as JSON.

        Args:
            country_to (str): Destination country name.

        Returns:
            str: JSON-serialized TravelResult dictionary.

        Example:
            >>> travel = TravelInfo("Israel")
            >>> json_str = travel.get_info("Japan")
            >>> isinstance(json.loads(json_str), dict)
            True
        """
        currency = CurrencyUtils.get_country_currency(country_to)

        exchange_rate = CurrencyUtils.get_exchange_rate(
            self.code_from,
            currency["currency_code"]
        )

        result: TravelResult = {
            "country_from": self.country_from,
            "country_to": country_to,
            "code_from": self.code_from,
            "code_to": currency["currency_code"],
            "currency_name": currency["currency_name"],
            "exchange_rate": exchange_rate,
        }

        return json.dumps(result)
