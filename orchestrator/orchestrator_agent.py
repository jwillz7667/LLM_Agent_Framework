# orchestrator/orchestrator_agent.py
from typing import Dict
from llm_integration_layer.request_router import RequestRouter
from llm_integration_layer.response_aggregator import ResponseAggregator
from contextual_knowledge_base.context_manager import ContextManager

class OrchestratorAgent:
    def __init__(self):
        self.request_router = RequestRouter()
        self.response_aggregator = ResponseAggregator()
        self.context_manager = ContextManager()

    def handle_task(self, task_data: Dict) -> Dict:
        # Get context from the knowledge base
        context = self.context_manager.get_context(task_data["project_id"])

        # Select the LLM provider based on task context (this logic can be expanded)
        provider = self._select_llm_provider(task_data, context)
        
        # Send request to the LLM Integration Layer
        response = self.request_router.route_request(provider, task_data)
        
        # Aggregate responses if needed (if using multiple providers)
        aggregated_response = self.response_aggregator.aggregate_responses([response])

        # Return the final response
        return aggregated_response

    def _select_llm_provider(self, task_data: Dict, context: Dict) -> str:
        # Placeholder logic for selecting LLM provider based on task and context
        # This can be expanded to include more complex decision-making
        return "openai" if "code_generation" in task_data["task_type"] else "anthropic"
