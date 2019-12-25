from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.config['SECRET_KEY'] = '93d76c3d2188e4980071b1198473d790'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from flask_blog import routes