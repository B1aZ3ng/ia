from game import Minecraft
import globals
from pathlib import Path
from game_utils import Installer
import json
from database import db, User, GameServer
from sqlalchemy import select

class GameCreator: #factory pattern to create the games

    def __init__(self):
        self.installer = Installer()
        with open("games.json") as file:
            self.games = json.load(file)
        print (self.games)


    def createGame(self, gameType, name, serverId, owner,serverType=None,version=None):

        if gameType not in self.games:
            raise Exception("Game does not exist")
        

        match gameType:
            case "Minecraft":
                serverTypes = self.games[gameType]
                if serverType not in serverTypes:
                    raise Exception("Server type does not exist")
                versions = serverTypes[serverType]
                if version not in versions:
                    raise Exception("Version does not exist")
                
                    
                path = globals.GAME_PATH / Path(str(serverId)+"/")
                path.mkdir(parents=True,exist_ok=True)

                download = self.games["Minecraft"][serverType][version]["download"]
                Installer.install_minecraft(download,path)
                return Minecraft("Minecraft " + serverType ,path,owner,serverId)

    def loadGame(self,gameType,name,path,owner,serverId):
        match gameType:
            case "Minecraft":
                return Minecraft(name,path,owner,serverId)


    def addToDB(self,name):
        pass

        
def loadGames():
    gc = GameCreator()
    for userId in db.session.execute(select(User.userId)):
        userId = userId[0] #because its a tuple for some reason like (1,) or (2,)...
        tmp = {}
        for serverId,serverName,serverPath,gameType in db.session.execute(select(GameServer.serverId,GameServer.serverName,GameServer.serverPath,GameServer.gameType).where(GameServer.ownerId == userId)):
            tmp[serverId] = gc.loadGame(gameType,serverName,serverPath,userId,serverId)
        globals.GAME_SERVERS[userId] = tmp
    