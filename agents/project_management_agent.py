# agents/project_management_agent.py
class ProjectManagementAgent:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_name: str, due_date: str):
        task = {
            "task_name": task_name,
            "due_date": due_date,
            "status": "pending"
        }
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def update_task_status(self, task_name: str, status: str):
        for task in self.tasks:
            if task["task_name"] == task_name:
                task["status"] = status

# Example usage
if __name__ == '__main__':
    agent = ProjectManagementAgent()
    agent.add_task("Complete code review", "2024-08-15")
    agent.add_task("Deploy new feature", "2024-08-20")
    tasks = agent.list_tasks()
    print(tasks)
    agent.update_task_status("Complete code review", "completed")
    print(agent.list_tasks())
