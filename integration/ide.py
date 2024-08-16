# integration/ide_integration.py
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.utils import format_request_data

class IDEIntegrationBase:
    def __init__(self):
        self.request_router = RequestRouter()

    def on_code_edit(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        prompt = f"Provide real-time feedback on the following code:\n{code_snippet}"
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

    def on_code_review(self, code_snippet: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        prompt = f"Review the following code for any issues:\n{code_snippet}"
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]
