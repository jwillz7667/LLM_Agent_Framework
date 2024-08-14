# contextual_knowledge_base/context_manager.py
class ContextManager:
    def __init__(self):
        self.contexts = {}

    def get_context(self, project_id: str) -> dict:
        return self.contexts.get(project_id, {})

    def update_context(self, project_id: str, context_data: dict):
        if project_id not in self.contexts:
            self.contexts[project_id] = {}
        self.contexts[project_id].update(context_data)

# Example usage
if __name__ == '__main__':
    manager = ContextManager()
    manager.update_context("project_123", {"language": "Python", "framework": "Django"})
    context = manager.get_context("project_123")
    print(context)
