from database import db, User, GameServer
import json
import subprocess
import requests
import os
from pathlib import Path
from game_utils import Installer,IOStream
import globals









class GameLoader:
    def __init__(self):
        pass
        

        


class Game: #blueprint
    def __init__(self,name,path,owner,id):
        self.name = name
        self.path = path
        self.owner = owner
        self.ios = None
        self.on = False
        self.gameType = "" # TBD
        self.id = id
        self.port = 6750 + id
        self.joinCmd = globals.IP_ADDRESS + ":" + str(self.port) # may change for each game


    def start(self): pass
    def stop(self): pass
    def isOn(self):
        if self.ios is None:
            return False
        else:
             return self.ios.is_alive()
    def status (self): return self.isOn()
    def get_name(self): return self.name
    def get_gameType(self): return self.gameType
    def get_path(self): return self.path
    def get_port(self): return self.port
    def get_id(self): return self.id
    def get_joinCmd(self): return self.joinCmd #join command
    def get_history(self):
        print (self.ios,self.ios.get_history())
        if self.status():
            return self.ios.get_history()
        else:
            return ""
    def send_command(self,line):
        self.ios.send_command(line)
    #def update(): pass


class Minecraft(Game):
    def __init__(self,name,path,owner,id):
        super().__init__(name,path,owner,id)
        self.gameType = "Minecraft"
        #self.joinCmd = globals.IP_ADDRESS + ":" + self.port 
        #^ is already declared in blueprint

    
    
    def start(self,func):
        if not self.status():
            self.ios = IOStream(self.path,["java", "-jar", "server.jar", "--nogui", "--port", str(self.port)])
            self.ios.read_output(func)
        
            

    def stop(self): 
        if self.status():
            self.ios.send_command("stop")
            
    
    

    



        

        
        
        

    def updateMinecraft():
        pass