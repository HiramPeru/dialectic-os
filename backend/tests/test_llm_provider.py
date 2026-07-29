import unittest
from types import SimpleNamespace

from app.intelligence.providers.factory import build_llm_provider
from app.intelligence.providers.openai_compatible import (
    LLMConfigurationError,
    LLMResponseError,
    OpenAICompatibleProvider,
    ProviderConfig,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeClient:
    def __init__(self, payload):
        self.payload = payload
        self.last_request = None

    def post(self, url, *, headers, json):
        self.last_request = {
            "url": url,
            "headers": headers,
            "json": json,
        }
        return FakeResponse(self.payload)


class OpenAICompatibleProviderTests(unittest.TestCase):
    def test_generate_sends_openai_compatible_request(self):
        client = FakeClient({
            "choices": [{"message": {"content": " Evidence-based result "}}],
        })
        provider = OpenAICompatibleProvider(
            ProviderConfig(
                name="nvidia",
                base_url="https://integrate.api.nvidia.com/v1",
                api_key="test-key",
                model="deepseek-ai/deepseek-v4-pro",
            ),
            client=client,
        )

        result = provider.generate("Compare these claims.")

        self.assertEqual(result, "Evidence-based result")
        self.assertEqual(
            client.last_request["url"],
            "https://integrate.api.nvidia.com/v1/chat/completions",
        )
        self.assertEqual(
            client.last_request["json"]["model"],
            "deepseek-ai/deepseek-v4-pro",
        )
        self.assertNotIn("test-key", str(client.last_request["json"]))

    def test_missing_api_key_fails_before_request(self):
        provider = OpenAICompatibleProvider(
            ProviderConfig(
                name="deepseek",
                base_url="https://api.deepseek.com",
                api_key=None,
                model="deepseek-v4-flash",
            ),
            client=FakeClient({}),
        )

        with self.assertRaisesRegex(
            LLMConfigurationError,
            "DEEPSEEK_API_KEY",
        ):
            provider.generate("Analyze.")

    def test_invalid_provider_response_is_rejected(self):
        provider = OpenAICompatibleProvider(
            ProviderConfig(
                name="nvidia",
                base_url="https://integrate.api.nvidia.com/v1",
                api_key="test-key",
                model="test-model",
            ),
            client=FakeClient({"choices": []}),
        )

        with self.assertRaises(LLMResponseError):
            provider.generate("Analyze.")

    def test_factory_selects_deepseek_defaults(self):
        provider = build_llm_provider(SimpleNamespace(
            LLM_PROVIDER="deepseek",
            LLM_MODEL=None,
            LLM_TIMEOUT_SECONDS=30,
            LLM_MAX_TOKENS=1000,
            NVIDIA_API_KEY=None,
            DEEPSEEK_API_KEY="test-key",
        ))

        self.assertEqual(provider.name, "deepseek")
        self.assertEqual(provider.model, "deepseek-v4-flash")
        self.assertEqual(provider.config.base_url, "https://api.deepseek.com")


if __name__ == "__main__":
    unittest.main()
