from flask import Flask, request, render_template
from flask_restful import Api, Resource, reqparse
from models import TasksModel, db
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to-do.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
app.app_context().push()

api = Api(app)
db.init_app(app)

with app.app_context():
    db.create_all()

class TasksView(Resource):
    def get(self):
        tasks = TasksModel.query.all()
        return {'Tasks': list(x.json() for x in tasks)}

    def post(self):
        data = request.get_json()
        new_tasks = TasksModel(data['content'])

        db.session.add(new_tasks)
        db.session.commit()
        db.session.flush()

        return new_tasks.json(), 201


class SingleTaskView(Resource):
    def get(self, id):
        task = TasksModel.query.filter_by(id=id).first()

        if task:
            return task.json()

        return {'message':'Task not found'}, 404

    def delete(self, id):
        task = TasksModel.query.filter_by(id=id).first()

        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message':'Task not found'}, 404

    def put(self, id):
        data = request.get_json()
        task = TasksModel.query.filter_by(id=id).first()

        if task:
            task.content = data['content']
        else:
            task = TasksModel(**data)

        db.session.add(task)
        db.session.commit()

        return task.json()

api.add_resource(TasksView, '/tasks')
api.add_resource(SingleTaskView, '/task/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=4500)