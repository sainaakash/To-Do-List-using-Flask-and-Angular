from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.app_context().push()

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duedate = db.Column(db.Date)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, duedate, content):
        self.duedate = datetime.strptime(duedate, '%Y-%m-%d')
        self.content = content
        self.done = False
        
    def __repr__(self):
        return "<Content %s>" % self.content

db.create_all()

@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    duedate = request.form.get('duedate')
    content = request.form['content']
    if not content and duedate:
        return 'Error'

    task = Task(duedate,content)
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


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, port=4500)
