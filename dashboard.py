import flask
from flask import Flask, render_template, request, redirect, session, flash, url_for
from database import db, User, GameServer
from sqlalchemy import select,update
import globals
from game_creator import GameCreator

gc = GameCreator()

dash = flask.Blueprint("dashboard", __name__)

@dash.route("/dashboard", methods=["GET","POST"])
def index():
    #print (globals.GAME_SERVERS)
    if not session.get("userId"):
        flash("You are not signed in")
        return redirect("login")
    id = session.get("userId")

    servers = []
    
    for key in globals.GAME_SERVERS[id]:
        sv = globals.GAME_SERVERS[id][key]        
        servers.append({"serverName":sv.get_name(),"gameType":sv.get_gameType(),"serverId":sv.get_id(),"running":sv.status(),"join":sv.get_joinCmd()})

    return render_template("dashboard.html",servers=servers,accountName=session.get("username"))

@dash.route("/dashboard/settings", methods=["GET","POST"])
def settings ():
    return render_template("dashboard_settings.html")


@dash.route("/dashboard/create",methods=["GET","POST"])
def create_server():
    if request.method == "POST":
        serverName = request.form.get("serverName")
        gameType = request.form.get("gameType")
        match gameType:
            case "Minecraft":

                serverType = request.form.get("serverType")
                version = request.form.get("version")
                newGame = GameServer(serverName=serverName, gameType=gameType, serverPath = None, ownerId = session.get("userId"))

                db.session.add(newGame)
                db.session.commit()

                serverId = newGame.serverId
                game = gc.createGame("Minecraft",serverName,serverId,session.get("userId"),serverType,version)

                newGame.serverPath = str(game.get_path())
                db.session.commit()

                globals.GAME_SERVERS[session.get("userId")][serverId] = game
        flash("Server Created")
        return redirect("/dashboard")
        


    return render_template("create_server.html",accountName=session.get("username"))


### functions for start/stop

