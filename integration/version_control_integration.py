# integration/version_control_integration.py
import subprocess
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.utils import format_request_data

class GitIntegration:
    def __init__(self):
        self.request_router = RequestRouter()

    def run_git_command(self, command: str) -> str:
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.output

    def generate_commit_message(self, diff: str, model: str = "gpt-4o", max_tokens: int = 150) -> str:
        prompt = f"Generate a commit message for the following diff:\n{diff}"
        request_data = format_request_data(prompt, max_tokens, model)
        response = self.request_router.route_request("openai", request_data)
        return response["text"]

# Example usage
if __name__ == '__main__':
    git_integration = GitIntegration()
    diff = git_integration.run_git_command("git diff")
    commit_message = git_integration.generate_commit_message(diff)
    print("Generated Commit Message:", commit_message)
