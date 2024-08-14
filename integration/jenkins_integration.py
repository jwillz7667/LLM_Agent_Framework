# integration/jenkins_integration.py
from .ci_cd_integration import CICDIntegrationBase

class JenkinsIntegration(CICDIntegrationBase):
    def __init__(self):
        super().__init__()

    def start_pipeline(self, pipeline_name: str) -> str:
        return self.trigger_pipeline(pipeline_name)

    def check_pipeline_status(self, pipeline_name: str) -> str:
        return self.monitor_pipeline(pipeline_name)

# Example usage
if __name__ == '__main__':
    jenkins_integration = JenkinsIntegration()
    start_response = jenkins_integration.start_pipeline("Deploy_Production")
    status_response = jenkins_integration.check_pipeline_status("Deploy_Production")
    print("Start Response:", start_response)
    print("Status Response:", status_response)
