# interface/flask_app.py

import sys
import os
from flask import Flask, render_template, request, jsonify

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.code_generation import CodeGenerationAgent
from agents.debugging import DebuggingAgent
from agents.code_review import CodeReviewAgent
from agents.testing import TestingAgent
from agents.project_management import ProjectManagementAgent
from core.request_router import RequestRouter

app = Flask(__name__)

# Initialize the request router and agents
router = RequestRouter()
code_generation_agent = CodeGenerationAgent(router)
debugging_agent = DebuggingAgent(router)
code_review_agent = CodeReviewAgent(router)
testing_agent = TestingAgent(router)
project_management_agent = ProjectManagementAgent(router)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_task', methods=['POST'])
def submit_task():
    task_type = request.form.get('task_type')
    input_data = request.form.get('input_data')
    model = request.form.get('model', 'gpt-4o')
    max_tokens = int(request.form.get('max_tokens', 100))

    try:
        if task_type == 'code_generation':
            result = code_generation_agent.generate_code(input_data, model, max_tokens)
        elif task_type == 'debugging':
            result = debugging_agent.debug_code(input_data, model, max_tokens)
        elif task_type == 'code_review':
            result = code_review_agent.review_code(input_data, model, max_tokens)
        elif task_type == 'testing':
            result = testing_agent.generate_tests(input_data, model, max_tokens)
        elif task_type == 'project_management':
            result = project_management_agent.manage_project(input_data, model, max_tokens)
        else:
            return jsonify({'error': 'Invalid task type'}), 400

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
