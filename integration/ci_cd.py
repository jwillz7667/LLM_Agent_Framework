# integration/ci_cd_integration.py
from core.request_router import RequestRouter
from core.utils import format_request_data

class CICDIntegrationBase:
    def __init__(self):
        self.request_router = RequestRouter()

    def trigger_pipeline(self, pipeline_name: str) -> str:
        prompt = f"Trigger the CI/CD pipeline: {pipeline_name}"
        request_data = format_request_data(prompt)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

    def monitor_pipeline(self, pipeline_name: str) -> str:
        prompt = f"Monitor the CI/CD pipeline: {pipeline_name} and report status."
        request_data = format_request_data(prompt)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]
