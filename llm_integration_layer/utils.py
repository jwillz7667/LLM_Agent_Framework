# llm_integration_layer/utils.py

import logging
import re

def setup_logging(log_level=logging.INFO):
    logging.basicConfig(level=log_level)
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    return logger

def format_request_data(prompt: str, max_tokens: int = 100, model: str = "gpt-4o") -> dict:
    return {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "model": model
    }

def handle_api_response(response):
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    return response.json()

def sanitize_input(input_string: str) -> str:
    # Remove any dangerous characters or patterns
    sanitized_string = re.sub(r'[^\w\s]', '', input_string)
    return sanitized_string

def validate_prompt(prompt: str):
    if len(prompt) > 500:
        raise ValueError("Prompt is too long.")
    if any(forbidden_word in prompt.lower() for forbidden_word in ["drop", "delete", "shutdown"]):
        raise ValueError("Prompt contains forbidden words.")
