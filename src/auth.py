import flask
from flask import Flask, render_template, request, redirect, session, flash,url_for

from database import db, User
from hashlib import sha256
from sqlalchemy import select



auth = flask.Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        passwordhash = sha256(request.form.get("password").encode('utf-8')).hexdigest() #hashes it sha256
        match_pwd_hash = db.session.execute(select(User.passwordHash).where(User.username == username)).first() #gets associated hashed pwd to username, if !exist then None
        if match_pwd_hash is None: #username not in database
            flash("Username does not exist")
            return render_template('login.html')
        elif match_pwd_hash[0]!=passwordhash: #need [0] becuase its outputs a set
            flash("Password is wrong")
            return render_template('login.html')
            

        else:
            session["username"] = username
            flash("Login succesful. Welcome, "+username)
            return redirect(url_for("index"))


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
            elif len(username)<1 or len(username)>16 or len(password1)<6 or len(password2)>32:
                flash("Username does not exist")   
                works = False  
            elif db.session.execute(select(User.passwordHash).where(User.username == username)).first() != None: #username exists in db
                flash("Username is already taken")  
                works = False

            if not works:
                return render_template('signup.html')
            else:
                passwordhash = sha256(password1.encode('utf-8')).hexdigest() #hashes it sha256
                newUser = User(username=username,passwordHash=passwordhash)
                db.session.add(newUser)
                db.session.commit()
                flash ("Account succesfully created for:", username)
                return redirect(url_for("index"))
                
    return render_template('signup.html')

