# core/request_router.py

# core/request_router.py

import time
from typing import Dict, Any
from cachetools import cached, TTLCache
from core.api_manager import APIManager
from core.exceptions import RateLimitExceededError, ProviderNotSupportedError
from core.utils import setup_logging, sanitize_input, validate_prompt
from llm_agent_framework.monitoring.prometheus_exporter import MonitoringExporter

# Initialize logging and monitoring
logger = setup_logging()
exporter = MonitoringExporter()

# Setup cache for API responses
cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 items for 5 minutes

class RequestRouter:
    def __init__(self, max_retries: int = 3, retry_delay: int = 2):
        self.supported_providers = ['openai']  # Only OpenAI is supported now
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_manager = APIManager()

    def route_request(self, provider: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        provider = sanitize_input(provider)
        validate_prompt(request_data.get('prompt', ''))

        if provider not in self.supported_providers:
            raise ProviderNotSupportedError(f"Provider {provider} is not supported.")

        for attempt in range(self.max_retries):
            try:
                return self._attempt_request(provider, request_data)
            except RateLimitExceededError as e:
                self._handle_rate_limit_error(e)
            except Exception as e:
                self._handle_general_error(e, attempt)

        raise Exception("Max retries reached. Failing.")

    @cached(cache, key=lambda self, provider, request_data: (provider, frozenset(request_data.items())))
    def _attempt_request(self, provider: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        api_key = self.api_manager.get_api_key(provider)

        with exporter.REQUEST_TIME.time():
            return self._query_openai(api_key, request_data)

    def _query_openai(self, api_key: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        import openai
        openai.api_key = api_key
        response = openai.Completion.create(
            model=request_data.get("model", "gpt-4o"),
            prompt=request_data['prompt'],
            max_tokens=request_data['max_tokens']
        )
        return {"text": response.choices[0].text}

    def _handle_rate_limit_error(self, e: RateLimitExceededError):
        exporter.record_error()
        logger.error(f"Rate limit error: {e}")
        time.sleep(self.retry_delay)

    def _handle_general_error(self, e: Exception, attempt: int):
        exporter.record_error()
        logger.error(f"Error during API request: {e}")
        if attempt < self.max_retries - 1:
            logger.info(f"Retrying... ({attempt + 1}/{self.max_retries})")
            time.sleep(self.retry_delay)
        else:
            logger.error("Max retries reached. Failing.")
