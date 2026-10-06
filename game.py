from database import db, User, GameServer
import json
import subprocess
import requests
import os
from pathlib import Path
from game_utils import IOStream,get_dir_size
import globals
import threading
import shutil








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
        self.storage=0
        self.refresh_storage()


    def start(self,func):             
        threading.Thread(target=self.ios.read_output,args=(func,),daemon=True).start()
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
        if self.status():
            return self.ios.get_history()
        else:
            return ""
    def send_command(self,line):
        self.ios.send_command(line)
    def get_memory_usage(self):
            if self.status():
                return self.ios.get_memory_usage()
            return 0
    def get_storage_usage(self):
        return self.storage
    
    # procedure to refresh the storage - done whenever server is started
    def refresh_storage(self):
        self.storage = get_dir_size(self.path)



class Minecraft(Game):
    def __init__(self,name,path,owner,id):
        print (name,path,owner,id)
        super().__init__(name,path,owner,id)
        self.gameType = "Minecraft"
        #self.joinCmd = globals.IP_ADDRESS + ":" + self.port 
        #^ is already declared in blueprint

    
    
    def start(self,func):
        if not self.status():
            self.ios = IOStream(self.path,["java", "-jar", "server.jar", "--nogui", "--port", str(self.port)])
        super().start(func)
        self.refresh_storage()
        
 

    def stop(self): 
        if self.status():
            self.ios.send_command("stop")
        self.refresh_storage() # refresh stored storage value

    

            
    
    

    



        

        
        
        

    def updateMinecraft():
        pass