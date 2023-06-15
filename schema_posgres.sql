/* cria a tabela */
DROP TABLE IF EXISTS tarefas;

CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title CHAR(50) NOT NULL,
    content CHAR(100) NOT NULL,
    dia data NOT NULL
);

/* insere dados iniciais */
INSERT INTO tarefas(title, content, dia) VALUES 
('First Post', 'Content for the first post', '20/11/2023');

INSERT INTO tarefas(title, content, dia) VALUES 
('Second Post', 'Content for the Second post', '24/11/2023');