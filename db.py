import sqlite3
import click 
from flask import current_app, g

#Criando conexao com o banco de dados
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['Database'], 
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

#inicia comandos SQL, do arquivo 'schema.sql'
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#cria um comando no console para iniciar o database
# > flask --app app init-db
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Database Initialized')

#registra banco de dados no app.py
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

#fecha chamada com o banco de dados
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()