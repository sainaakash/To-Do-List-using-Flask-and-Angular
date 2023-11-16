from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProductModel(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    

    def __init__(self,content):
        self.content = content

    def json(self):
        return {"id":self.id, "content":self.content}


