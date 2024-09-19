CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    descricao TEXT DEFAULT " ",
    completed BOOLEAN NOT NULL DEFAULT 0
);

INSERT INTO tasks (title, descricao, completed) VALUES
    ('Exemplo 1', 'Antes do cafe da manha', 0),
    ('Exemplo 2', 'Depois do almoco', 1);

