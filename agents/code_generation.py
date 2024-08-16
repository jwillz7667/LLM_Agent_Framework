# agents/code_generation.py

from typing import Dict, Any
from core.request_router import RequestRouter
from core.utils import sanitize_input, validate_prompt

class CodeGenerationAgent:
    def __init__(self, router: RequestRouter):
        self.router = router

    def generate_code(self, prompt: str, model: str = "gpt-4o", max_tokens: int = 100) -> Dict[str, Any]:
        """
        Generates code based on the provided prompt using the specified model.

        :param prompt: The prompt for code generation.
        :param model: The model to use for code generation.
        :param max_tokens: The maximum number of tokens to generate.
        :return: The generated code.
        """
        prompt = sanitize_input(prompt)
        validate_prompt(prompt)

        request_data = {
            "prompt": prompt,
            "model": model,
            "max_tokens": max_tokens
        }

        return self.router.route_request(provider="openai", request_data=request_data)