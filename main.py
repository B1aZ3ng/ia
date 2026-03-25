from src import auth
from flask import Flask


app = Flask(__name__)
app.register_blueprint(auth.Auth)

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)