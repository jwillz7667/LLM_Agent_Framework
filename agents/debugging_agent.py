# agents/debugging_agent.py
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.utils import format_request_data

class DebuggingAgent:
    def __init__(self):
        self.request_router = RequestRouter()

    def debug_code(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        prompt = f"Find and fix any bugs in the following Python code:\n{code_snippet}"
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

# Example usage
if __name__ == '__main__':
    agent = DebuggingAgent()
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)
"""
    fixed_code = agent.debug_code(code)
    print(fixed_code)
