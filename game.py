

GAME_PATH = "games_tmp/"
from database import db, User, gameServer
import json
import subprocess
import requests

class GameCreator: #factory pattern to create the games

    def __init__(self):
        with open("games.json") as file:
            self.games = json.load(file)
        print (self.games)


    def create_game(self, gameName, name, owner,serverType=None,version=None):

        if gameName not in self.games:
            raise Exception("Game does not exist")
        serverTypes = self.games[gameName]
        if serverType not in serverTypes:
            raise Exception("Server type does not exist")

        versions = serverTypes[serverType]
        if version not in versions:
            raise Exception("Version does not exist")
        if gameName == "Minecraft":
            self.setup_minecraft(gameName,name,owner,serverType,owner)
        raise Exception("Unsupported game")

    def setup_minecraft(self, gameName, name, owner,serverType,version):
        download = self.games[gameName][serverType][version]["download"]
        

    def update_minecraft():
        pass
        


class GameLoader:
    def __init__(self):
        pass
        

        


class Game: #blueprint
    def __init__(self,name,path,owner):
        self.name = name
        self.path = path
        self.owner = owner
        self.isOn = False

    
    def start(): pass
    def stop(): pass
    def update(): pass

class Minecraft(Game):
    def __init__(self,name,path,owner,version):
        super().__init__(name,path,owner)
        self.version = version

    



