# ./src/utils/currency_utils.py

import os
from typing import TypedDict
from .json_utils import JSONUtils


class CurrencyInfo(TypedDict):
    """
    Typed dictionary representing currency details.

    Attributes:
        currency_code (str): ISO currency code, e.g., 'USD'.
        currency_name (str): Full currency name, e.g., 'United States Dollar'.

    Example:
        >>> info: CurrencyInfo = {
                "currency_code": "USD",
                "currency_name": "United States Dollar"
            }
        >>> info["currency_code"]
        'USD'
    """
    currency_code: str
    currency_name: str


class CurrencyUtils:
    """
    Utility class for retrieving country currency information and
    calculating exchange rates using RestCountries and Fixer APIs.

    Example:
        >>> CurrencyUtils.get_country_currency("Israel")
        {'currency_code': 'ILS', 'currency_name': 'Israeli New Shekel'}
        >>> CurrencyUtils.calculate_cross_rate(1.0, 3.5)
        3.5
    """

    RESTCOUNTRIES_URL = "https://restcountries.com/v3.1/name/"
    FIXER_API_URL = "http://data.fixer.io/api/latest"
    FIXER_API_KEY = os.getenv("FIXER_API_KEY")

    @staticmethod
    def get_country_currency(country: str) -> CurrencyInfo:
        """
        Retrieve currency information for a given country.

        Args:
            country (str): Name of the country.

        Returns:
            CurrencyInfo: Dictionary containing 'currency_code'
                          and 'currency_name'.

        Raises:
            ValueError: If the country or currency data is not found
                        or invalid.

        Example:
            >>> CurrencyUtils.get_country_currency("Japan")
            {'currency_code': 'JPY', 'currency_name': 'Japanese yen'}
        """
        data = JSONUtils.get_data(
            f"{CurrencyUtils.RESTCOUNTRIES_URL}{country}"
        )

        if not isinstance(data, list) or not data:
            raise ValueError(f"Country '{country}' not found.")

        country_data = data[0]
        currencies = country_data.get("currencies")

        if not isinstance(currencies, dict) or not currencies:
            raise ValueError(f"No currency information for '{country}'.")

        code = next(iter(currencies))
        currency_data = currencies[code]

        if not isinstance(currency_data, dict) or "name" not in currency_data:
            raise ValueError(f"Invalid currency structure for '{country}'.")

        return CurrencyInfo(
            currency_code=code,
            currency_name=currency_data["name"],
        )

    @staticmethod
    def get_exchange_rate(code_from: str, code_to: str) -> float:
        """
        Calculate exchange rate from one currency to another using Fixer API.

        Args:
            code_from (str): Source currency code.
            code_to (str): Target currency code.

        Returns:
            float: Exchange rate rounded to 2 decimal places.

        Raises:
            RuntimeError: If FIXER_API_KEY is not set.
            ValueError: If Fixer API returns an error or missing rates.

        Example:
            >>> CurrencyUtils.get_exchange_rate("USD", "EUR")
            0.94
        """
        if not CurrencyUtils.FIXER_API_KEY:
            raise RuntimeError("Fixer API key not set in environment")

        params = {"access_key": CurrencyUtils.FIXER_API_KEY}
        data = JSONUtils.get_data(
            url=CurrencyUtils.FIXER_API_URL,
            params=params
        )

        if not data.get("success", False):  # type: ignore
            raise ValueError(f"Fixer API returned an error: {data}")

        rates = data.get("rates")     # type: ignore
        if not rates or not isinstance(rates, dict):
            raise ValueError("Invalid rates data from Fixer API")

        rate_from = rates.get(code_from)
        rate_to = rates.get(code_to)

        if rate_from is None or rate_to is None:
            raise ValueError(
                f"Exchange rate not available for {code_from} or {code_to}"
            )

        return CurrencyUtils.calculate_cross_rate(rate_from, rate_to)

    @staticmethod
    def calculate_cross_rate(rate_from: float, rate_to: float) -> float:
        """
        Calculate cross rate from source to target currency.

        Args:
            rate_from (float): Rate of source currency.
            rate_to (float): Rate of target currency.

        Returns:
            float: Cross rate rounded to 2 decimals.

        Example:
            >>> CurrencyUtils.calculate_cross_rate(1.0, 3.5)
            3.5
        """
        return round(float(rate_to) / float(rate_from), 2)
