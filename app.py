from flask import Flask, jsonify, redirect, request
from flask_openapi3 import OpenAPI, Tag
import db #importa o banco de dados
from flask_cors import CORS

#comentario teste
app = OpenAPI(__name__)
app.config['Database'] = 'tasks.db'
CORS(app)

#inicia banco de dados
db.init_app(app)

@app.route('/')
def index():
    return redirect('/openapi')

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


#Rota para pegar tasks do banco de dados e passar para o front 
@app.route('/tasks', methods=['GET'], tags=[home_tag])
def select_tasks():
    print("In route tasks")
    db_conn = db.get_db() 
    tasks = db_conn.execute(
        'SELECT id, title, descricao, completed FROM tasks'
    ).fetchall()

    #transformar em uma lista de dicionarios para passar para JSON
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
@app.route('/insert', methods=['POST'], tags=[produto_tag])
def insert_task():
    title = request.form['title']
    description = request.form['description']
    completed = False

    #Connexao com o banco de dados, sempre mesmo padrao
    db_conn = db.get_db()
    db_conn.execute(
        'INSERT INTO tasks (title, descricao, completed) VALUES (?, ?, ?)',
        (title, description, completed)
    )
    db_conn.commit()

#Deletar tarefas ja feitas, deixas tarefas que ainda nao foram resolvidas
@app.route('/end-day', methods=['DELETE'])
def end_day():
    db_conn = db.get_db()
    db_conn.execute(
        'DELETE FROM tasks WHERE completed = 1'
    )
    db_conn.commit()
    return {'message': 'Completed tasks deleted'}, 200

#Atualiza tarefas feitas
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