from flask import Flask, jsonify, request
from tasks import Task

app = Flask(__name__)

tasks = [
    Task(1, 'Wash dishes', 'Do the dishes tonight', False),
    Task(2, 'Do Laundry', 'Do laundry tomorrow morning', True),
]

API_KEY = 'snoop'

@app.before_request
def authenticate_request():
    if request.endpoint != 'get_all_tasks' and request.headers.get('Api-Key') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    return jsonify([vars(task) for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(vars(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(len(tasks) + 1, data['title'], data['description'], data['completed'])
    tasks.append(new_task)
    return jsonify(vars(new_task)), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        return jsonify(vars(task))
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task.id != task_id]
    return jsonify({'result': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)