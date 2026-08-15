from database import db, User, GameServer
import json
import subprocess
import requests
import os
from pathlib import Path
from game_utils import Installer,IOStream
from globals import *







#TESTING
# if __name__ == "__main__":

#     gc = GameCreator()

#     gc.create_game('Minecraft','mctest',1,'Paper','26.1.2')
class GameCreator: #factory pattern to create the games

    def __init__(self):
        self.installer = Installer()
        with open("games.json") as file:
            self.games = json.load(file)
        print (self.games)


    def createGame(self, gameType, name, id, owner,serverType=None,version=None):

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
                
                    
                path = GAME_PATH / Path(str(id)+"/")
                path.mkdir(parents=True,exist_ok=True)

                download = self.games["Minecraft"][serverType][version]["download"]
                Installer.install_minecraft(download,path)
                return Minecraft(name,"Minecraft " + serverType ,path,owner)

    def loadGame(self,gameType,name,path,owner):
        match gameType:
            case "Minecraft":
                return Minecraft(name,path,owner)


    def addToDB(self,name):
        pass


class GameLoader:
    def __init__(self):
        pass
        

        


class Game: #blueprint
    def __init__(self,name,gameType,path,owner):
        self.name = name
        self.path = path
        self.owner = owner
        self.ios = None
        self.on = False
        self.gameType = gameType
    
    def start(self): pass
    def stop(self): pass
    def isOn(self): return self.on

    def getName(self): return self.name
    def getGameType(self): return self.gameType
    def getPath(self): return self.path
    #def update(): pass

class Minecraft(Game):
    def __init__(self,name,gameType,path,owner):
        super().__init__(name,gameType,path,owner)
        
    
    def start(self):
        if not self.on:
            self.ios = IOStream(self.path,["java", "-jar", "server.jar", "--nogui"])
            self.on = True

    def stop(self):
        if self.ios:
            self.ios.send_command("stop")
            self.on = False


    



        

        
        
        

    def updateMinecraft():
        pass