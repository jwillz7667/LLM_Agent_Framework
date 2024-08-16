# agents/debugging.py

from typing import Dict, Any
from core.request_router import RequestRouter
from core.utils import sanitize_input, validate_prompt

class DebuggingAgent:
    def __init__(self, router: RequestRouter):
        self.router = router

    def debug_code(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 100) -> Dict[str, Any]:
        """
        Analyzes and debugs a code snippet using the specified model.

        :param code_snippet: The code snippet to debug.
        :param model: The model to use for debugging.
        :param max_tokens: The maximum number of tokens for the debugging output.
        :return: The debugging output.
        """
        code_snippet = sanitize_input(code_snippet)
        validate_prompt(code_snippet)

        request_data = {
            "prompt": f"Debug the following code:\n{code_snippet}",
            "model": model,
            "max_tokens": max_tokens
        }

        return self.router.route_request(provider="openai", request_data=request_data)