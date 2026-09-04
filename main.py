from flask import Flask, render_template
from database import db,User,GameServer
import auth
import dashboard
import globals
from sqlalchemy import select
#from game import GameCreator
from game_creator import loadGames



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.secret_key = "49d180ecf56132819571bf39d9b7b342522a2ac6d23c1418d3338251bfe469c8" #idk flask.flash() needs it, its sha256 of 67 lol

app.register_blueprint(auth.auth)
app.register_blueprint(dashboard.dash)


@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        loadGames()
    
    
    app.run(host="0.0.0.0", port=25565, debug=True)



