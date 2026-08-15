from flask import Flask, render_template
from database import db,User,GameServer
import auth
import dashboard
import globals
from sqlalchemy import select
from game import GameCreator    


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.secret_key = "49d180ecf56132819571bf39d9b7b342522a2ac6d23c1418d3338251bfe469c8" #idk flask.flash() needs it, its sha256 of 67 lol

app.register_blueprint(auth.auth)
app.register_blueprint(dashboard.dash)


@app.route("/")
def index():
    return render_template("index.html")

def loadGames():
    gc = GameCreator()
    for userId in db.session.execute(select(User.userId)):
        userId = userId[0]
        tmp = {}
        for serverId,serverName,serverPath,gameType in db.session.execute(select(GameServer.serverId,GameServer.serverName,GameServer.serverPath,GameServer.gameType)):
            tmp[serverId] = gc.loadGame(gameType,serverName,serverPath)
        globals.GAME_SERVERS[userId] = tmp
    print ('six seven')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        loadGames()
    
    
    app.run(debug=True)



