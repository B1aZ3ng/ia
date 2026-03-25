from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

class User(db.Model):
    userId = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(16), unique=True, nullable=False)
    passwordHash = mapped_column(String(64), nullable=False)

class gameServer(db.Model):
    serverId = mapped_column(Integer, primary_key=True)
    serverName = mapped_column(String(16), unique=True, nullable=False)
    serverLocation = mapped_column(String(256), nullable=False)
    userId = mapped_column(Integer, db.ForeignKey('user.userId'), nullable=False)


with app.app_context():
    db.create_all()