# agents/project_management.py

from typing import Dict, Any
from core.request_router import RequestRouter
from core.utils import sanitize_input, validate_prompt

class ProjectManagementAgent:
    def __init__(self, router: RequestRouter):
        self.router = router

    def manage_project(self, task_description: str, model: str = "gpt-4o", max_tokens: int = 100) -> Dict[str, Any]:
        """
        Provides project management guidance based on a given task description.

        :param task_description: A description of the project management task.
        :param model: The model to use for generating guidance.
        :param max_tokens: The maximum number of tokens for the guidance output.
        :return: The project management guidance.
        """
        task_description = sanitize_input(task_description)
        validate_prompt(task_description)

        request_data = {
            "prompt": f"Provide project management guidance for the following task:\n{task_description}",
            "model": model,
            "max_tokens": max_tokens
        }

        return self.router.route_request(provider="openai", request_data=request_data)