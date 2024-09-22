from typing import Optional
from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Tag
import db #importa o banco de dados
from flask_cors import CORS
from pydantic import BaseModel

#comentario teste
app = OpenAPI(__name__)
app.config['Database'] = 'tasks.db'
CORS(app)

#inicia banco de dados
db.init_app(app)

@app.route('/')
def index():
    return redirect('/openapi')

# Definindo uma tag
task_tag = Tag(name="Task", description="Operações relacionadas às tarefas")

# Schemas usando Pydantic
class TaskSchema(BaseModel):
    title: str
    description: str
    completed: bool

class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

#Rota para pegar tasks do banco de dados e passar para o front 
@app.get('/tasks', tags=[task_tag], responses={"200": TaskResponseSchema})
def select_tasks():
    """
    Faz a busca de todas as tasks existentes
    """
    
    print("In route tasks")
    db_conn = db.get_db()
    tasks = db_conn.execute(
        'SELECT id, title, descricao, completed FROM tasks'
    ).fetchall()

    tasks_list = []
    for task in tasks:
        tasks_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['descricao'],
            'completed': task['completed']
        })

    return jsonify(tasks_list)

#Rota para inserir um terefa no banco de dados
@app.post('/insert', tags=[task_tag], responses={"200": TaskSchema})
def insert_task(form: TaskSchema):
    """
    Adiona uma tarefa ao banco de dados
    """
    
    title = request.form.get('title')
    description = request.form.get('description')
    completed = False  # Definir como False por padrão, já que novas tarefas começam não completadas

    # Conexão com o banco de dados
    db_conn = db.get_db()
    db_conn.execute(
        'INSERT INTO tasks (title, descricao, completed) VALUES (?, ?, ?)',
        (title, description, completed)
    )
    db_conn.commit()

    return {"message": "Task created successfully"}, 201

#Deletar tarefas ja feitas, deixas tarefas que ainda nao foram resolvidas
@app.delete('/end-day')
def end_day():
    """
    Termina o dia deletando tarefas que ja foram completadas
    """
    db_conn = db.get_db()
    db_conn.execute(
        'DELETE FROM tasks WHERE completed = 1'
    )
    db_conn.commit()
    return {'message': 'Completed tasks deleted'}, 200

#Atualiza tarefas feitas
@app.route('/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Faz o update de uma tarefa pra completa ou incompleta
    """
    try:
        print(f"Received request to update task with ID: {task_id}")
        
        # Access the JSON body
        data = request.json
        completed = data.get('completed')
        
        # Here you would typically update your database
        db_conn = db.get_db()
        db_conn.execute('UPDATE tasks SET completed = ? WHERE id = ?', (completed, task_id))
        db_conn.commit()
        
        return jsonify({"message": "Task Updated Successfully"}), 200
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        return jsonify({"error": str(e)}), 500