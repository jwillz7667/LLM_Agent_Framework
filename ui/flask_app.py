# ui/flask_app.py
from flask import Flask, render_template, request, redirect, url_for
from orchestrator.task_manager import TaskManager

app = Flask(__name__)
task_manager = TaskManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_task', methods=['POST'])
def submit_task():
    task_type = request.form['task_type']
    prompt = request.form['prompt']
    task_manager.add_task({
        "task_id": 1,  # In a real application, this would be dynamically generated
        "task_type": task_type,
        "project_id": "project_123",
        "prompt": prompt
    })
    task_manager.start_task_processor()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
