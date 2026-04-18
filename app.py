from flask import Flask, render_template, request, redirect, url_for
from FLASK.config import Config
from FLASK.extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from FLASK.models import Todo

@app.route('/', methods=["GET"])
def get_todos():
    allTodo = Todo.query.order_by(Todo.date_created.desc()).all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/', methods=["POST"])
def add_todo():
    title = request.form.get('title', '').strip()
    desc = request.form.get('desc', '').strip()

    if not title or not desc:
        return "Title and Description cannot be empty"

    todo = Todo(title=title, desc=desc)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('get_todos'))

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'This is products page'

@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)

    if request.method == "POST":
        title = request.form.get('title', '').strip()
        desc = request.form.get('desc', '').strip()

        if not title or not desc:
            return "Fields cannot be empty"

        todo.title = title
        todo.desc = desc

        db.session.commit()
        return redirect(url_for('get_todos'))

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('get_todos'))

with app.app_context():
    db.create_all()