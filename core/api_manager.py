# core/api_manager.py

import os
import logging
import boto3
import json
from typing import Dict
from threading import Lock
from core.exceptions import InvalidEnvironmentError, APIKeyError

class APIManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(APIManager, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.api_keys = self._load_api_keys_from_secrets_manager()
        self.rate_limits = {
            'openai': 60,  # Define rate limits per provider (only OpenAI here)
        }
        self.request_count = {key: 0 for key in self.api_keys.keys()}
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _load_api_keys_from_secrets_manager(self) -> Dict[str, str]:
        if self.environment not in ["development", "staging", "production"]:
            raise InvalidEnvironmentError(f"Invalid environment: {self.environment}")

        client = boto3.client('secretsmanager')
        secret_name = f"llm_api_keys_{self.environment}"
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

    def get_api_key(self, provider: str) -> str:
        if provider != 'openai':
            self.logger.error(f"No API key available for provider: {provider}")
            raise APIKeyError(f"Provider {provider} not supported.")
        return self.api_keys[provider]

    def increment_request_count(self, provider: str):
        if provider in self.request_count:
            self.request_count[provider] += 1
            self.logger.info(f"Request count for {provider}: {self.request_count[provider]}")

    def check_rate_limit(self, provider: str) -> bool:
        if self.request_count[provider] >= self.rate_limits[provider]:
            self.logger.warning(f"Rate limit exceeded for {provider}.")
            return False
        return True

    def reset_request_count(self, provider: str):
        self.request_count[provider] = 0
        self.logger.info(f"Request count reset for {provider}.")

# Singleton pattern to ensure only one APIManager instance exists
api_manager = APIManager()
