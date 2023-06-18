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
    ('Task 1', 'Description for Task 1', '2023-06-20'),
    ('Task 2', 'Description for Task 2', '2023-06-22'),
    ('Task 3', 'Description for Task 3', '2023-06-25');