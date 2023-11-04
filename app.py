from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///to-do.db'
app.app_context().push()

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False
        
    def __repr__(self):
        return "<Content %s>" % self.content

db.create_all()

"""
@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while creating the task'

    else:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)
"""

@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
