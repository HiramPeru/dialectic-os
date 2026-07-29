from functools import lru_cache
from typing import Protocol

from app.core.config import Settings, settings
from app.intelligence.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderConfig,
)


class ProviderSettings(Protocol):
    LLM_PROVIDER: str
    LLM_MODEL: str | None
    LLM_TIMEOUT_SECONDS: float
    LLM_MAX_TOKENS: int
    NVIDIA_API_KEY: str | None
    DEEPSEEK_API_KEY: str | None


PROVIDER_DEFAULTS = {
    "nvidia": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model": "deepseek-ai/deepseek-v4-pro",
        "key_field": "NVIDIA_API_KEY",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-v4-flash",
        "key_field": "DEEPSEEK_API_KEY",
    },
}


def build_llm_provider(
    provider_settings: ProviderSettings,
) -> OpenAICompatibleProvider:
    provider_name = provider_settings.LLM_PROVIDER.lower()
    provider_defaults = PROVIDER_DEFAULTS[provider_name]
    api_key = getattr(provider_settings, provider_defaults["key_field"])

    return OpenAICompatibleProvider(
        ProviderConfig(
            name=provider_name,
            base_url=provider_defaults["base_url"],
            api_key=api_key,
            model=provider_settings.LLM_MODEL or provider_defaults["model"],
            timeout_seconds=provider_settings.LLM_TIMEOUT_SECONDS,
            max_tokens=provider_settings.LLM_MAX_TOKENS,
        )
    )


@lru_cache(maxsize=1)
def get_llm_provider() -> OpenAICompatibleProvider:
    return build_llm_provider(settings)


def generate_text(
    prompt: str,
    *,
    system_prompt: str = "You are a precise intelligence analyst.",
) -> str:
    return get_llm_provider().generate(
        prompt,
        system_prompt=system_prompt,
    )


def get_llm_status(provider_settings: Settings = settings) -> dict[str, object]:
    provider = build_llm_provider(provider_settings)
    return {
        "provider": provider.name,
        "model": provider.model,
        "configured": bool(provider.config.api_key),
    }
