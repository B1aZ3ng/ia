import flask
from flask import Flask, render_template, request, redirect, session, flash,url_for
import dashboard
from database import db, User, GameServer
from hashlib import sha1
from sqlalchemy import select
from game_creator import loadGames


auth = flask.Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        
        
        if not db.session.scalar(db.select(db.exists().where(User.username == username))):# username not in database #username not in database
            flash("Username does not exist")
            return render_template('login.html')

        passwordhash = sha1(request.form.get("password").encode('utf-8')).hexdigest() #hashes it sha256
        match_pwd_hash = db.session.execute(select(User.passwordHash).where(User.username == username)).scalar_one() #gets associated hashed pwd to username, if !exist then None

        if match_pwd_hash != passwordhash: #need [0] becuase its outputs a set
            flash("Password is wrong")
            return render_template('login.html')
        else:
            session["username"] = username
            session["userId"] = db.session.execute(select(User.userId).where(User.username == username)).scalar_one()
            flash("Login succesful. Welcome, "+username)
            return redirect(url_for("dashboard.index"))


    return render_template('login.html')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
            username = request.form.get("username")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            works = True #bc so many conditions better to just use a boolean
            if password1 != password2:
                flash("Passwords do not match")
                works = False
            elif len(username)<1 or len(username)>16 or len(password1)<4 or len(password2)>32:
                flash("does not meet requrirements")   
                works = False  
            elif db.session.execute(select(User.passwordHash).where(User.username == username)).scalar() != None: #username exists in db
                flash("Username is already taken")  
                works = False

            if not works:
                return render_template('signup.html')
            else:
                passwordhash = sha1(password1.encode('utf-8')).hexdigest() #hashes it sha256
                newUser = User(username=username,passwordHash=passwordhash)
                db.session.add(newUser)
                db.session.commit()
                flash ("Account succesfully created for:", username)
                loadGames
                return redirect(url_for("index"))
                
    return render_template('signup.html')


def loadSession(userId):
    userServers = db.session.execute(select(GameServer.serverName,GameServer.serverPath).where(GameServer.ownerID == userId))
    