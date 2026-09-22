#generated with chatgpt to test stuff 
#redo manually
from flask import Flask, render_template, Blueprint,session, redirect,flash,url_for
from flask_socketio import SocketIO, join_room, emit
from pathlib import Path
import threading
import game_utils
import globals
from console import send_log
import filebrowser.app
from game_utils import IOStream



server = Blueprint("server", __name__,url_prefix="/server")
server.register_blueprint(filebrowser.app.fb) 


def authenticate(serverId): #returns a redirect function if theres
    if "userId" not in session: #if not logged in
        flash("You are not logged in")
        return redirect(url_for("/login"))
    if serverId not in globals.GAME_SERVERS[session.get("userId")]: #if logged in but accesses a server thats not like their own
        flash("Not your server")
        return redirect(url_for("/dashboard"))
    return None



@server.route("/<int:serverId>/console")
def index(serverId):
    redir = authenticate(serverId)
    if redir: return redir
    return render_template("console.html",serverId = serverId)



@server.route("/<int:serverId>/start", methods=["POST"])
def start_server(serverId):
    redir = authenticate(serverId)
    if redir: return redir
    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    room = "room_" + str(serverId)
    server.start(lambda x: send_log(x,room)) #never thought i'd use lambda functions ever again
    return redirect("/dashboard")


@server.route("/<int:serverId>/stop", methods=["POST"])
def stop_server(serverId):
    redir = authenticate(serverId)
    if redir: return redir
    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    server.stop()
    return redirect("/dashboard")


