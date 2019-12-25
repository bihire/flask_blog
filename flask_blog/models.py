from datetime import datetime
from flask_blog import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), unique=True, nullable= False)
    password = db.Column(db.String(32), nullable= False)
    image_file = db.Column(db.String(120), nullable= False,  default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcfromtimestamp)
    content = db.Column(db.Text, nullable=False)
    user_id= db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.created_on}')"