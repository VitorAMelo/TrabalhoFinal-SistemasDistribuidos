/* cria a tabela */
DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE
);

/* insere dados iniciais */
INSERT INTO tasks (title, description, due_date) VALUES
    ('Tarefa 1', 'Fazer comida', '2023-06-20'),
    ('Tarefa 2', 'tomar banho', '2023-06-22'),
    ('Tarefa 3', 'Fazer trabalho', '2023-06-25');