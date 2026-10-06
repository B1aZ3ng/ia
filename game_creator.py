from game import Minecraft
import globals
from pathlib import Path
import json
from database import db, User, GameServer
from sqlalchemy import select,delete
import requests
import shutil
class GameCreator: #factory pattern to create the games
    def __init__(self):
        with open("games.json") as file:
            self.games = json.load(file)
        #print (self.games)

    def createGame(self, gameType, name, serverId, owner,serverType=None,version=None):
        if gameType not in self.games:
            raise Exception("Game does not exist")
        match gameType:
            case "Minecraft":
                serverTypes = self.games[gameType]
                #input validation
                if serverType not in serverTypes:  
                    raise Exception("Server type does not exist")
                versions = serverTypes[serverType]
                if version not in versions:
                    raise Exception("Version does not exist")
                
                #creates the directory to install
                path = globals.GAME_PATH / Path(str(serverId)+"/")
                path.mkdir(parents=True,exist_ok=True)

                #downloads it
                download = self.games["Minecraft"][serverType][version]["download"]
                self.install_minecraft(download,path)
                return Minecraft(name,path,owner,serverId)
            case "Terreria":
                ...
            case "CS2":
                ...
            case "Unturned":
                ...

    def loadGame(self,gameType,name,path,owner,serverId):
        match gameType:
            case "Minecraft":
                return Minecraft(name,path,owner,serverId)
            case "Terreria":
                ...
            case "CS2":
                ...
            case "Unturned":
                ...

    def install_minecraft(self,download,path): #download link #make sure ios already is in path of game file
        print("downloading...")
        response = requests.get(download)
        if response.status_code == 200:
            with open(path / Path("server.jar"), "wb") as f:
                f.write(response.content)
        
        print("initialising...")

        with open(path / Path("eula.txt"), "w") as f:
            f.write("eula=true\n")
        print ("done")
    def delete_game(self,userId,serverId):
        server = globals.GAME_SERVERS[userId][serverId]
        #stop if running
        server.stop()
        # remove from db
        cmd = delete(GameServer).where(GameServer.serverId == serverId)
        db.session.execute(cmd)
        db.session.commit()
        #delete from location
        shutil.rmtree(server.path)
        # delete from dict
        globals.GAME_SERVERS[userId].pop(serverId)
        
        # delete from memory
        del server

        return cmd



        
def load_games():
    gc = GameCreator()
    for userId in db.session.execute(select(User.userId)):
        userId = userId[0] #because its a tuple for some reason like (1,) or (2,)...
        tmp = {}
        for serverId,serverName,serverPath,gameType in db.session.execute(select(GameServer.serverId,GameServer.serverName,GameServer.serverPath,GameServer.gameType).where(GameServer.ownerId == userId)):
            tmp[serverId] = gc.loadGame(gameType,serverName,serverPath,userId,serverId)
        globals.GAME_SERVERS[userId] = tmp
    