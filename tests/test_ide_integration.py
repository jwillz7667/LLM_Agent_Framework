# tests/test_ide_integration.py
import unittest
from integration.vscode_integration import VSCodeIntegration

class TestVSCodeIntegration(unittest.TestCase):

    def setUp(self):
        self.vscode_integration = VSCodeIntegration()

    def test_provide_feedback(self):
        code = "def factorial(n): return n * factorial(n - 1)"
        feedback = self.vscode_integration.provide_feedback(code)
        self.assertIn("feedback", feedback.lower())

    def test_provide_review(self):
        code = "def factorial(n): return n * factorial(n - 1)"
        review = self.vscode_integration.provide_review(code)
        self.assertIn("review", review.lower())

if __name__ == '__main__':
    unittest.main()
