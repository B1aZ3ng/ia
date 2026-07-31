from flask import Flask, render_template
from database import db
from src import auth



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

app.secret_key = "49d180ecf56132819571bf39d9b7b342522a2ac6d23c1418d3338251bfe469c8" #idk flask.flash() needs it, its sha256 of 67 lol

app.register_blueprint(auth.auth)


@app.route("/")
def index():
    return render_template("main.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)