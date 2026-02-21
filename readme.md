# Homework 39 – Travel Currency Information & Exchange Rate Tool

## Task Definition

The goal of Homework 39 is to **enhance the `TravelInfo` tool** by refactoring JSON extraction and integrating real-time currency exchange rate calculation using the **Fixer.io API**.

Specifically, the task requires:

1. Updating the `TravelInfo.get_info()` method:
    - Extract lines 11–19 into a universal helper function `extract_json`.
    - `extract_json` should accept a text string and a list of expected JSON properties:
        ```py
        extract_json(text: str, properties: list[str]) -> dict
        ```
        Example usage:
        - Extract tool call JSON: `extract_json(text, ["tool", "arguments"])`
        - Extract currency information JSON: `extract_json(text, ["country", "currency_code"])`

2. Implement additional function(s) for fetching the exchange rate from `code_from` to `code_to`.

3. Integrate **Fixer.io API**:
    - Use free access key to fetch latest rates via `http://data.fixer.io/api/latest?access_key=<API_KEY>`.
    - Fill the `exchange_rate` property in `TravelInfo.get_info()` result with the proper value.

---

## 📝 Description

This project provides a **Python-based travel assistant tool** that:

- Returns currency information between origin and destination countries.
- Computes live exchange rates using the Fixer.io API.
- Extracts structured JSON from arbitrary text using a robust helper function.

Key components:

- **`TravelInfo` class** – provides travel currency info and exchange rates.
- **`JSONUtils.extract_json`** – generic JSON extractor.
- **`CurrencyUtils`** – fetches currency codes and computes exchange rates.
- **CLI interface** – interacts with the user via `AgentCLI` and LLM integration.

Project structure:

```

./src/
├─ main.py              # Entry point and CLI launcher
├─ agent/               # LLM agent, CLI, tool orchestration
├─ tools/               # TravelInfo and tool routing utilities
└─ utils/               # JSON and currency helpers

```

---

## 🎯 Purpose

The project focuses on:

1. **Refactoring and modularization** – Extracting repeated logic into reusable helper functions (`extract_json`).
2. **API integration** – Using Fixer.io to obtain live currency exchange rates.
3. **Data modeling** – Returning structured JSON (`TravelResult`) for easy consumption.
4. **Real-world LLM tooling** – Enabling structured tool calls from LLM responses.

By combining structured tool results and external API integration, this project provides a **reliable travel currency assistant**.

---

## 🔍 How It Works

1. **Initialization**
    - `TravelInfo` is initialized with the origin country (e.g., Israel).
    - `CurrencyUtils` reads the Fixer.io API key from environment variables (`FIXER_API_KEY`).

2. **Fetching Currency Information**
    - `get_info(country_to)` retrieves destination currency metadata.
    - Uses `extract_json` to parse JSON embedded in LLM responses.

3. **Calculating Exchange Rate**
    - `CurrencyUtils.get_exchange_rate(code_from, code_to)` fetches latest rates from Fixer.io.
    - Populates `exchange_rate` in the resulting JSON.

4. **Error Handling**
    - Raises exceptions for missing API keys, invalid countries, or unavailable exchange rates.
    - Ensures `extract_json` returns `None` if required properties are not found.

---

## 📜 Output Example

### ✅ Valid country

```py
from tools.travel import TravelInfo

travel = TravelInfo("Israel")
info = travel.get_info("Japan")
print(info)
```

Output:

```json
{
	"country_from": "Israel",
	"country_to": "Japan",
	"code_from": "ILS",
	"code_to": "JPY",
	"currency_name": "Yen",
	"exchange_rate": 40.5
}
```

### ❌ Invalid country

```py
info = travel.get_info("UnknownCountry")
# → ValueError: Country 'UnknownCountry' not found.
```

---

## 📦 Usage

```py
from tools.travel import TravelInfo

travel = TravelInfo("Israel")
destination = "France"
travel_info = travel.get_info(destination)
print(travel_info)
```

### CLI Interaction

```bash
python -m src.main
```

- Type any travel-related query.
- LLM returns structured JSON calling the `travel_info.get_info` tool.
- Example:

```
You: Travel to Japan
Agent: {"tool": "travel_info.get_info", "arguments": {"country_to": "Japan"}}
```

---

## ✅ Dependencies

- Python 3.10+
- `requests`
- `python-dotenv` (for environment variable loading)
- Fixer.io API key (`FIXER_API_KEY`)

---

## 📊 Project Status

**Status:** ✅ Completed

- Refactored `TravelInfo.get_info()` with reusable `extract_json`.
- Integrated Fixer.io API for live exchange rates.
- Structured JSON response for all travel queries.
- Fully compatible with CLI and LLM-based agent.

---

## 📄 License

MIT License

---

## 🧮 Conclusion

This project demonstrates:

- Modular JSON extraction via `extract_json`.
- Real-time currency exchange integration with Fixer.io.
- Structured, reliable travel information output.
- Ready-to-use CLI and LLM agent integration.

---

Made with ❤️ and `Python` by **Sam-Shepsl Malikin** 🎓
