CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    descricao TEXT,
    completed BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO tasks (title, descricao, completed) VALUES
    ('Tarefa 1', 'Descricao da tarefa 1', 0),
    ('Tarefa2', 'Descricao da tarefa 2', 1);

