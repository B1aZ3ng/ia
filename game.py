from database import db, User, GameServer
import json
import subprocess
import requests
import os
from pathlib import Path
from game_utils import Installer,IOStream
from globals import *









class GameLoader:
    def __init__(self):
        pass
        

        


class Game: #blueprint
    def __init__(self,name,path,owner):
        self.name = name
        self.path = path
        self.owner = owner
        self.ios = None
        self.on = False
        self.gameType = "" # TBD
    
    def start(self): pass
    def stop(self): pass
    def isOn(self): return self.on

    def getName(self): return self.name
    def getGameType(self): return self.gameType
    def getPath(self): return self.path
    #def update(): pass


class Minecraft(Game):
    def __init__(self,name,path,owner):
        super().__init__(name,path,owner)
        self.gameType = "Minecraft"
        
    
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