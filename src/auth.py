import flask
from flask import Flask, render_template



Auth = flask.Blueprint('auth', __name__)

@Auth.route('/auth')
def login():
    return render_template('login_page.html')

