#generated with chatgpt to test stuff 
#redo manually
from flask import Flask, render_template, Blueprint,session, redirect,flash,url_for,Response,jsonify
from flask_socketio import SocketIO, join_room, emit
from pathlib import Path
import threading
import globals
from console import send_log
import filebrowser.app
from game_creator import GameCreator


server = Blueprint("server", __name__,url_prefix="/server")
server.register_blueprint(filebrowser.app.fb) 




@server.before_request
def authenticate(*args):
    if "userId" not in session: #if not logged in
            flash("You are not logged in")
            return redirect(url_for("auth.login"))
    if args:
        serverId = args[0]
        if serverId not in globals.GAME_SERVERS[session.get("userId")]: #if logged in but accesses a server thats not like their own
                flash("Not your server")
                return redirect(url_for("dash.index"))

@server.route("/<int:serverId>/console")
def index(serverId):
    return render_template("console.html",serverId = serverId)



@server.route("/<int:serverId>/start", methods=["POST"])
def start_server(serverId):
    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    room = "room_" + str(serverId)
    server.start(lambda x: send_log(x,room)) #never thought i'd use lambda functions ever again - basically creates the function specific to each room
    return Response("ok",status=200)


@server.route("/<int:serverId>/stop", methods=["POST"])
def stop_server(serverId):
    redir = authenticate(serverId)
    if redir: return redir

    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    server.stop()
    return Response("ok",status=200) #does not mean its succesful


@server.route("/<int:serverId>/update")
def update(serverId):
    redir = authenticate(serverId)
    if redir: return redir
    
    sv = globals.GAME_SERVERS[session.get("userId")][serverId]
    print(sv.get_storage_usage())
    data = {"running": sv.status(),
            "memory": round(sv.get_memory_usage()/(10**9),2),
            "storage": round(sv.get_storage_usage()/(10**9),2),
            }
    return jsonify(data)

@server.route("/<int:serverId>/settings")
def settings(serverId):
    return render_template("server_settings.html",serverId=serverId)


@server.route("/<int:serverId>/delete")
def delete(serverId):
    gc = GameCreator()
    gc.delete_game(session.get("userId"),serverId)
    return redirect("/dashboard")