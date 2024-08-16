# core/response_aggregator.py

from typing import List, Dict, Any  # Ensure Any is imported

class ResponseAggregator:
    def aggregate_responses(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        aggregated = {"results": []}
        for response in responses:
            aggregated["results"].append(response.get("text", ""))
        return aggregated
