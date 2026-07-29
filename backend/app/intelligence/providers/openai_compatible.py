from dataclasses import dataclass
from typing import Any, Protocol

import httpx


class HTTPClient(Protocol):
    def post(
        self,
        url: str,
        *,
        headers: dict[str, str],
        json: dict[str, Any],
    ) -> httpx.Response: ...


class LLMProviderError(RuntimeError):
    """Base error for model-provider failures."""


class LLMConfigurationError(LLMProviderError):
    """Raised when the selected provider is not configured."""


class LLMRequestError(LLMProviderError):
    """Raised when the provider request fails."""


class LLMResponseError(LLMProviderError):
    """Raised when a provider returns an unusable response."""


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    api_key: str | None
    model: str
    timeout_seconds: float = 180.0
    max_tokens: int = 4096


class OpenAICompatibleProvider:
    """Minimal client shared by NVIDIA NIM and DeepSeek APIs."""

    def __init__(
        self,
        config: ProviderConfig,
        client: HTTPClient | None = None,
    ) -> None:
        self.config = config
        self._client = client

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def model(self) -> str:
        return self.config.model

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str = "You are a precise intelligence analyst.",
        temperature: float = 0.2,
    ) -> str:
        if not self.config.api_key:
            key_name = (
                "NVIDIA_API_KEY"
                if self.config.name == "nvidia"
                else "DEEPSEEK_API_KEY"
            )
            raise LLMConfigurationError(
                f"{key_name} is required for provider '{self.config.name}'."
            )

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": self.config.max_tokens,
            "stream": False,
        }

        try:
            headers = {
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            }
            if self._client:
                response = self._client.post(
                    url,
                    headers=headers,
                    json=payload,
                )
            else:
                with httpx.Client(
                    timeout=self.config.timeout_seconds,
                ) as client:
                    response = client.post(
                        url,
                        headers=headers,
                        json=payload,
                    )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise LLMRequestError(
                f"{self.config.name} request failed: {exc}"
            ) from exc

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMResponseError(
                f"{self.config.name} returned an invalid chat completion."
            ) from exc

        if not isinstance(content, str) or not content.strip():
            raise LLMResponseError(
                f"{self.config.name} returned an empty chat completion."
            )

        return content.strip()
