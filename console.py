from flask_socketio import SocketIO, join_room
from flask import session
import globals
socketio = SocketIO(cors_allowed_origins="*")

def send_log(line,room):
    print(line, end="")
    socketio.emit("console_output",{"message": line},to=room)


def read_server_output(server):
    server.read_output(send_log) 
    if not server.isOn():
        socketio.emit("server_status", {"online": False})


@socketio.on("join")
def handle_connect(data):
    serverId = int(data["serverId"])
    room = "room_" + str(serverId)
    join_room(room) #one room for each server, as theres no way for flask to know otherwise which server their sending and receiving data from
    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    history = server.get_history()
    
    if not server.status():
        socketio.emit("server_status", {"online": False})
        return    
    socketio.emit("server_status", {"online": True})
    socketio.emit("console_history", {"messages": history})


@socketio.on("command")
def command(data):
    cmd = data.get("command", "").strip() #formats the command
    serverId = int(data["serverId"])
    if not cmd: return
    server = globals.GAME_SERVERS[session.get("userId")][serverId]
    if not server.status():
        socketio.emit( "server_status",{"online": False})
        return
    #print("Command:", cmd)
    server.send_command(cmd)
