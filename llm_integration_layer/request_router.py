# llm_integration_layer/request_router.py

import time
from typing import Dict
from cachetools import cached, TTLCache
from llm_integration_layer.api_manager import APIManager
from llm_integration_layer.exceptions import RateLimitExceededError, ProviderNotSupportedError
from llm_integration_layer.utils import setup_logging
from llm_agent_framework.monitoring.prometheus_exporter import MonitoringExporter

# Initialize logging and monitoring
logger = setup_logging()
exporter = MonitoringExporter()

# Setup cache for API responses
cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 items for 5 minutes

class RequestRouter:
    def __init__(self, max_retries=3, retry_delay=2):
        self.supported_providers = ['openai', 'anthropic', 'llama3']
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_manager = APIManager()

    def route_request(self, provider: str, request_data: Dict) -> Dict:
        if provider not in self.supported_providers:
            raise ProviderNotSupportedError(f"Provider {provider} is not supported.")
        
        for attempt in range(self.max_retries):
            try:
                if not self.api_manager.check_rate_limit(provider):
                    raise RateLimitExceededError(f"Rate limit exceeded for provider: {provider}.")
                
                with exporter.REQUEST_TIME.time():
                    api_key = self.api_manager.get_api_key(provider)
                    response = self._send_request(provider, api_key, request_data)
                    self.api_manager.increment_request_count(provider)
                    return response
            
            except RateLimitExceededError as e:
                exporter.record_error()
                logger.error(f"Rate limit error: {e}")
                time.sleep(self.retry_delay)
            
            except Exception as e:
                exporter.record_error()
                logger.error(f"Error during API request: {e}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying... ({attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Max retries reached. Failing.")
                    raise

    @cached(cache)
    def _send_request(self, provider: str, api_key: str, request_data: Dict) -> Dict:
        if provider == 'openai':
            return self._query_openai(api_key, request_data)
        elif provider == 'anthropic':
            return self._query_anthropic(api_key, request_data)
        elif provider == 'llama3':
            return self._query_llama3(api_key, request_data)
    
    def _query_openai(self, api_key: str, request_data: Dict) -> Dict:
        import openai
        openai.api_key = api_key
        response = openai.Completion.create(
            model=request_data.get("model", "gpt-4o"),
            prompt=request_data['prompt'],
            max_tokens=request_data['max_tokens']
        )
        return {"text": response.choices[0].text}

    def _query_anthropic(self, api_key: str, request_data: Dict) -> Dict:
        import anthropic
        client = anthropic.Client(api_key=api_key)
        response = client.completions.create(
            model=request_data.get("model", "claude-sonnet-3.5"),
            prompt=request_data['prompt'],
            max_tokens=request_data['max_tokens']
        )
        return {"text": response['completion']}