# locustfile.py

from locust import HttpUser, task, between

class LLMFrameworkUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def submit_task(self):
        self.client.post("/submit_task", json={
            "task_type": "code_generation",
            "prompt": "Write a Python function to reverse a string."
        })

    @task
    def check_status(self):
        self.client.get("/status")
