# agents/testing.py

from typing import Dict, Any
from core.request_router import RequestRouter
from core.utils import sanitize_input, validate_prompt

class TestingAgent:
    def __init__(self, router: RequestRouter):
        self.router = router

    def generate_tests(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 100) -> Dict[str, Any]:
        """
        Generates test cases for a given code snippet using the specified model.

        :param code_snippet: The code snippet to generate tests for.
        :param model: The model to use for generating tests.
        :param max_tokens: The maximum number of tokens for the test output.
        :return: The generated test cases.
        """
        code_snippet = sanitize_input(code_snippet)
        validate_prompt(code_snippet)

        request_data = {
            "prompt": f"Generate unit tests for the following code:\n{code_snippet}",
            "model": model,
            "max_tokens": max_tokens
        }

        return self.router.route_request(provider="openai", request_data=request_data)