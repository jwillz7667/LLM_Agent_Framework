# agents/code_review_agent.py
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.utils import format_request_data

class CodeReviewAgent:
    def __init__(self):
        self.request_router = RequestRouter()

    def review_code(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        prompt = f"Review the following Python code for best practices, readability, and security vulnerabilities:\n{code_snippet}"
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

# Example usage
if __name__ == '__main__':
    agent = CodeReviewAgent()
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
"""
    review = agent.review_code(code)
    print(review)
