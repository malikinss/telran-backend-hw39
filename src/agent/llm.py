# ./src/agent/llm.py

import os
import requests
from typing import Final
from .common_data_types import Messages, Payload


URL_ENV: Final[str] = "PHI3_API_URL"
MODEL_ENV: Final[str] = "PHI3_MODEL_NAME"


class LLMClient:
    """
    Thin HTTP client for communicating with the Phi-3 LLM API.

    Responsibilities:
        - Read configuration from environment variables.
        - Send conversation history to the LLM endpoint.
        - Return assistant textual reply.
        - Fail fast on invalid configuration or malformed responses.

    Non-responsibilities:
        - Prompt construction
        - Tool logic
        - Message validation
        - Retry strategies

    Environment Variables:
        PHI3_API_URL      - Full HTTP endpoint URL
        PHI3_MODEL_NAME   - Model identifier

    Example:
        >>> import os
        >>> os.environ["PHI3_API_URL"] = "http://localhost:8000/chat"
        >>> os.environ["PHI3_MODEL_NAME"] = "phi-3"
        >>> client = LLMClient()
        >>> isinstance(client.url, str)
        True
    """

    def __init__(self) -> None:
        """
        Initialize client from environment variables.

        Raises:
            RuntimeError:
                If required environment variables are missing.
        """
        self.url: str | None = os.getenv(URL_ENV)
        self.model: str | None = os.getenv(MODEL_ENV)

        if not self.url:
            raise RuntimeError(
                f"Environment variable '{URL_ENV}' is not set."
            )

        if not self.model:
            raise RuntimeError(
                f"Environment variable '{MODEL_ENV}' is not set."
            )

    def send(self, messages: Messages) -> str:
        """
        Send conversation history to LLM and return assistant reply.

        Contract:
            - messages must be ordered chronologically
            - each message must contain 'role' and 'content'
            - response must contain 'message.content'

        Args:
            messages (Messages):
                Full conversation history.

        Returns:
            str:
                Assistant response text.

        Raises:
            requests.HTTPError:
                If API returns non-2xx status.
            ValueError:
                If response JSON structure is invalid.
            requests.RequestException:
                On network errors.
        """
        payload: Payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        url: str = self.url   # type: ignore
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()

        try:
            content = data["message"]["content"]
        except (KeyError, TypeError):
            raise ValueError(
                "Invalid response structure: \
                    expected data['message']['content']."
            )

        if not isinstance(content, str):
            raise ValueError("LLM response content must be a string.")

        return content
