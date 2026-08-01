from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)



class User(db.Model):
    userId = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(16), unique=True, nullable=False)
    passwordHash = mapped_column(String(64), nullable=False)


class gameServer(db.Model):
    serverId = mapped_column(Integer, primary_key=True)
    serverName = mapped_column(String(16), unique=True, nullable=False)
    serverPath = mapped_column(String(256), nullable=False)
    ownerID = mapped_column(Integer, db.ForeignKey("user.userId"), nullable=False)