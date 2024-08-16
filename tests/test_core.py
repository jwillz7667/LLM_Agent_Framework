# tests/test_llm_integration.py
import unittest
from llm_integration_layer.api_manager import APIManager
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.response_aggregator import ResponseAggregator
from llm_integration_layer.exceptions import RateLimitExceededError, ProviderNotSupportedError

class TestLLMIntegrationLayer(unittest.TestCase):

    def setUp(self):
        self.api_manager = APIManager()
        self.request_router = RequestRouter()
        self.response_aggregator = ResponseAggregator()

    def test_api_key_retrieval(self):
        self.assertIsNotNone(self.api_manager.get_api_key('openai'))
        self.assertIsNotNone(self.api_manager.get_api_key('anthropic'))
        self.assertIsNotNone(self.api_manager.get_api_key('llama3'))

    def test_rate_limit(self):
        self.assertTrue(self.api_manager.check_rate_limit('openai'))

    def test_provider_support(self):
        with self.assertRaises(ProviderNotSupportedError):
            self.request_router.route_request('unsupported_provider', {})

    def test_response_aggregation(self):
        responses = [{"text": "Hello, world!"}, {"text": "Goodbye, world!"}]
        aggregated = self.response_aggregator.aggregate_responses(responses)
        self.assertIn("Hello, world!", aggregated["combined_text"])
        self.assertIn("Goodbye, world!", aggregated["combined_text"])

if __name__ == '__main__':
    unittest.main()
