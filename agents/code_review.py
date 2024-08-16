# agents/code_review.py

from typing import Dict, Any
from core.request_router import RequestRouter
from core.utils import sanitize_input, validate_prompt

class CodeReviewAgent:
    def __init__(self, router: RequestRouter):
        self.router = router

    def review_code(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 100) -> Dict[str, Any]:
        """
        Reviews a code snippet and provides feedback or suggestions.

        :param code_snippet: The code snippet to review.
        :param model: The model to use for the code review.
        :param max_tokens: The maximum number of tokens for the review output.
        :return: The review output.
        """
        code_snippet = sanitize_input(code_snippet)
        validate_prompt(code_snippet)

        request_data = {
            "prompt": f"Review the following code:\n{code_snippet}",
            "model": model,
            "max_tokens": max_tokens
        }

        return self.router.route_request(provider="openai", request_data=request_data)