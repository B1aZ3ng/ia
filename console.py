#generated with chatgpt to test stuff 
#redo manually
from flask import Flask, render_template
from flask_socketio import SocketIO
from pathlib import Path
import threading

from game_utils import IOStream


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

#testing::
server = IOStream(
    Path("games_tmp/67/"),
    ["java", "-jar", "server.jar", "--nogui"]
)


def send_log(line):
    #print(line, end="")
    socketio.emit("console_output",{"message": line})



def read_server_output(server):
    server.read_output(send_log)
    if not server.isOn():
        socketio.emit("server_status", {"online": False})


threading.Thread(
    target=read_server_output,daemon=True).start()



@app.route("/")
def index():
    return render_template("console.html")



@socketio.on("connect")
def handle_connect():
    if not server.is_alive():
        socketio.emit("server_status", {"online": False})
        return

    
    socketio.emit("server_status", {"online": True})

    
    history = server.get_history()

    socketio.emit("console_history", {"messages": history})


@socketio.on("command")
def command(data):
    cmd = data.get("command", "").strip()
    if not cmd: return
    
    if not server.is_alive():
        socketio.emit( "server_status",{"online": False})
        return
    print("Command:", cmd)
    server.send_command(cmd)



# if __name__ == "__main__":
#     socketio.run(
#         app,
#         host="0.0.0.0",
#         port=5001,
#         debug=False
#     )