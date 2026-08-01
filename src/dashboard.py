import flask
from flask import Flask, render_template, request, redirect, session, flash, url_for






dash = flask.Blueprint('dashboard', __name__)

@dash.route('/dashboard', methods=['GET','POST'])
def dashboard ():
    return render_template('dashboard.html')

@dash.route('/dashboard', methods=['GET','POST'])
def dashboard_settings ():
    return render_template('dashboard_settings.html')
