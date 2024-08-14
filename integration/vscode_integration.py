# integration/vscode_integration.py
from .ide_integration import IDEIntegrationBase

class VSCodeIntegration(IDEIntegrationBase):
    def __init__(self):
        super().__init__()

    def provide_feedback(self, code_snippet: str) -> str:
        return self.on_code_edit(code_snippet)

    def provide_review(self, code_snippet: str) -> str:
        return self.on_code_review(code_snippet)

# Example usage
if __name__ == '__main__':
    vscode_integration = VSCodeIntegration()
    code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
"""
    feedback = vscode_integration.provide_feedback(code)
    review = vscode_integration.provide_review(code)
    print("Feedback:", feedback)
    print("Review:", review)
