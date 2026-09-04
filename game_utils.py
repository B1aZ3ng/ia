
import requests
from pathlib import Path
from database import db, GameServer, User
import subprocess
import os
import hashlib
import re
import urllib.request
import pty
import threading
from collections.abc import Sequence
from collections import deque
import time
import globals
import json
from sqlalchemy import select
#from game_factory import GameCreator


     
class IOStream:
    def __init__(self, path, command, max_log_lines=10000):
        self.history = deque(maxlen=max_log_lines)
        self.lock = threading.Lock()

        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=path,
            bufsize=1
        )

    def send_command(self, command):
        if self.process.poll() is None:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

    def is_alive(self):
        return self.process.poll() is None

    def get_history(self):
        with self.lock:
            return list(self.history)

    def read_output(self, func):
        for line in self.process.stdout:
            with self.lock:
                self.history.append(line)

            func(line)




class Installer:
    

    @staticmethod
    def addToDB(id,name,gameType,path,ownerID):
        new_game = GameServer(
            serverId = id,
            serverName = name,
            gameType = gameType,
            serverPath = path,
            ownerID = ownerID,
        )
        db.session.add(new_game)
        db.session.commit()
    
    @staticmethod    
    def install_minecraft(download,path): #download link #make sure ios already is in path of game file
        print("downloading...")
        response = requests.get(download)
        if response.status_code == 200:
            with open(path / Path("server.jar"), "wb") as f:
                f.write(response.content)
        
        print("initialising...")
    
        with open(path / Path("eula.txt"), "w") as f:
            f.write("eula=true\n")
        print ("done")
        


        



