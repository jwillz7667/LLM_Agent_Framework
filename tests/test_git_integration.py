# tests/test_git_integration.py
import unittest
from integration.version_control_integration import GitIntegration

class TestGitIntegration(unittest.TestCase):

    def setUp(self):
        self.git_integration = GitIntegration()

    def test_run_git_command(self):
        result = self.git_integration.run_git_command("git --version")
        self.assertIn("git version", result.lower())

    def test_generate_commit_message(self):
        diff = "diff --git a/file.py b/file.py"
        commit_message = self.git_integration.generate_commit_message(diff)
        self.assertIn("commit", commit_message.lower())

if __name__ == '__main__':
    unittest.main()
