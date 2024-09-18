from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI
import db
from flask_cors import CORS


app = OpenAPI(__name__)
app.config['Database'] = 'tasks.db'
CORS(app)

@app.route('/')
def index():
    return redirect('/openapi')

@app.route('/tasks', methods=['GET'])
def select_tasks():
    print("In route tasks")
    db_conn = db.get_db()  # Get the database connection
    tasks = db_conn.execute(
        'SELECT id, title, descricao, completed FROM tasks'
    ).fetchall()

    # Convert tasks into a list of dictionaries to return as JSON
    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['descricao'],
            'completed': task['completed']
        })

    return jsonify(tasks_list)

@app.route('/insert', methods=['POST'])
def insert_task():
    title = request.form['title']
    description = request.form['description']
    completed = False

    db_conn = db.get_db()
    db_conn.execute(
        'INSERT INTO tasks (title, descricao, completed) VALUES (?, ?, ?)',
        (title, description, completed)
    )
    db_conn.commit()

@app.route('/end-day', methods=['POST'])
def end_day():
    db_conn = db.get_db()
    db_conn.execute(
        'DELETE FROM tasks WHERE completed = 1'
    )
    db_conn.commit()
    return {'message': 'Completed tasks deleted'}, 200

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    data = request.json
    completed = data.get('completed')

    db_conn = db.get_db()  # Get the database connection
    db_conn.execute(
        'UPDATE tasks SET completed = ? WHERE id = ?',
        (completed, task_id)
    )
    db_conn.commit()  # Commit the transaction

    return jsonify({"message": "Task Updated Successfully"})

db.init_app(app)
