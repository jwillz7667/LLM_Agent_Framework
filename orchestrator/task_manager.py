# orchestrator/task_manager.py
import queue
from threading import Thread
from typing import Dict
from .orchestrator_agent import OrchestratorAgent

class TaskManager:
    def __init__(self):
        self.task_queue = queue.Queue()
        self.orchestrator_agent = OrchestratorAgent()

    def add_task(self, task_data: Dict):
        self.task_queue.put(task_data)

    def process_tasks(self):
        while not self.task_queue.empty():
            task_data = self.task_queue.get()
            result = self.orchestrator_agent.handle_task(task_data)
            self._handle_task_result(task_data, result)

    def _handle_task_result(self, task_data: Dict, result: Dict):
        # Placeholder function for handling task results
        # This could involve storing results, triggering further actions, etc.
        print(f"Task {task_data['task_id']} processed with result: {result}")

    def start_task_processor(self):
        worker_thread = Thread(target=self.process_tasks)
        worker_thread.start()

# Example usage
if __name__ == '__main__':
    task_manager = TaskManager()
    task_manager.add_task({
        "task_id": 1,
        "task_type": "code_generation",
        "project_id": "project_123",
        "prompt": "Write a function to calculate the Fibonacci sequence."
    })
    task_manager.start_task_processor()
