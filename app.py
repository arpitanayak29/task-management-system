from flask import Flask, render_template, request, redirect
from db import get_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    search = request.args.get('search')

    if search:
        cursor.execute("SELECT * FROM tasks WHERE title LIKE %s", ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()
    conn.close()

    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['GET','POST'])
def add_task():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        remarks = request.form['remarks']
        created_by = request.form['created_by']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO tasks
        (title,description,due_date,status,remarks,created_by,updated_by)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """,(title,description,due_date,status,remarks,created_by,created_by))

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_task.html')


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_task(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        remarks = request.form['remarks']
        updated_by = request.form['updated_by']

        cursor.execute("""
        UPDATE tasks
        SET title=%s,description=%s,due_date=%s,status=%s,
        remarks=%s,updated_by=%s
        WHERE id=%s
        """,(title,description,due_date,status,remarks,updated_by,id))

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute("SELECT * FROM tasks WHERE id=%s",(id,))
    task = cursor.fetchone()

    return render_template('edit_task.html',task=task)


@app.route('/delete/<int:id>')
def delete_task(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=%s",(id,))
    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)