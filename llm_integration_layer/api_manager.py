# llm_integration_layer/api_manager.py

import os
import logging
import boto3
import json
from typing import Dict
from threading import Lock

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
        self.api_keys = self._load_api_keys_from_secrets_manager()
        self.rate_limits = {
            'openai': 60,  # 60 requests per minute as an example
            'anthropic': 60,
            'llama3': 60
        }
        self.request_count = {key: 0 for key in self.api_keys.keys()}
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _load_api_keys_from_secrets_manager(self) -> Dict[str, str]:
        client = boto3.client('secretsmanager')
        secret_name = "llm_api_keys"
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)

    def get_api_key(self, provider: str) -> str:
        if provider not in self.api_keys:
            self.logger.error(f"No API key available for provider: {provider}")
            raise ValueError(f"Provider {provider} not supported.")
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

# Singleton pattern is used to ensure only one APIManager instance exists
api_manager = APIManager()
