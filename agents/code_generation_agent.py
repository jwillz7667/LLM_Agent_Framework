# agents/code_generation_agent.py
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.utils import format_request_data

class CodeGenerationAgent:
    def __init__(self):
        self.request_router = RequestRouter()

    def generate_code(self, prompt: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

# Example usage
if __name__ == '__main__':
    agent = CodeGenerationAgent()
    code = agent.generate_code("Write a Python function that calculates the factorial of a number.")
    print(code)
