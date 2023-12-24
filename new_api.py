# Partner Programming - Christian Toro

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Task API!'})

API_KEY = 'JTC'

def authenticate():
    with app.app_context():
        if request.endpoint != 'static':
            if 'Authorization' not in request.headers or request.headers['Authorization'] != API_KEY:
                return jsonify({'error': 'Unauthorized Access...Who are you?'}), 401
            
@app.before_request
def before_request():
    authenticate()

@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([task.__dict__ for task in tasks])
    
    elif request.method == 'POST':
        data = request.get_json()
        if 'title' not in data or 'completed' not in data:
            return jsonify({'error': 'Missing required information!'}), 400
        
        new_task = Task(
            title=data['title'], 
            description=data.get('description', ''), 
            completed=data['completed']
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.__dict__), 201
    
@app.route('/tasks/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found!'}), 404
    
    if request.method == 'GET':
        return jsonify(task.__dict__)
    
    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data['title']
        task.description = data.get('description', '')
        task.completed = data['completed']
        db.session.commit()
        return jsonify(task.__dict__)
    
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'}), 200
    
with app.app_context():
    db.create_all()

def run():
    with app.app_context():
        app.run(debug=True)
        
if __name__ == '__main__':
    run()