import os
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import datetime
from datetime import timedelta

# cria a conexao com o BD
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="tasks",
        user=os.getenv('DB_USERNAME'),
        password=os.environ['DB_PASSWORD']
    )
    return conn

# query todas as tarefas no banco
def get_task(task_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE id = %s', (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()
    return task

# cria o serviço
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET_KEY_DEV')

# definicao das rotas
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks ORDER BY due_date ASC')
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    current_date = datetime.utcnow()  # Atualize para datetime.datetime.utcnow()
    return render_template('index.html', tasks=tasks, current_date=current_date, timedelta=timedelta)

@app.route('/<int:task_id>')
def task(task_id):
    task = get_task(task_id)
    if task is None:
        return render_template('404.html')
    return render_template('task.html', task=task, current_date=datetime.now().date())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO tasks (title, description, due_date) VALUES (%s, %s, %s)',
                         (title, description, due_date))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    task = get_task(id)

    if task is None:
        return render_template('404.html')

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('UPDATE tasks SET title = %s, description = %s, due_date = %s WHERE id = %s',
                         (title, description, due_date, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', task=task)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    task = get_task(id)
    if task is None:
        return render_template('404.html')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash(f'"{task[1]}" was successfully deleted.')
    return redirect(url_for('index'))

# inicia servico
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
