# llm_integration_layer/response_aggregator.py
from typing import List, Dict

class ResponseAggregator:
    def __init__(self):
        pass

    def aggregate_responses(self, responses: List[Dict]) -> Dict:
        aggregated_response = {"combined_text": ""}
        for response in responses:
            aggregated_response["combined_text"] += response["text"] + "\n"
        return aggregated_response
