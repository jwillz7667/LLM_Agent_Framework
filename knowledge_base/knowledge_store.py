# contextual_knowledge_base/knowledge_store.py
import json
import os

class KnowledgeStore:
    def __init__(self, storage_path="context_store.json"):
        self.storage_path = storage_path
        self._load_contexts()

    def _load_contexts(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                self.contexts = json.load(f)
        else:
            self.contexts = {}

    def save_context(self, project_id: str, context_data: dict):
        self.contexts[project_id] = context_data
        with open(self.storage_path, "w") as f:
            json.dump(self.contexts, f)

    def get_context(self, project_id: str) -> dict:
        return self.contexts.get(project_id, {})

# Example usage
if __name__ == '__main__':
    store = KnowledgeStore()
    store.save_context("project_123", {"language": "Python", "framework": "Django"})
    context = store.get_context("project_123")
    print(context)
