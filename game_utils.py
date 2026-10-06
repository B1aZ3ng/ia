import psutil
import requests
from pathlib import Path
from database import db, GameServer
import subprocess
import threading
from collections import deque
import os


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
        return (self.process.poll() is None)

    def get_history(self):
        with self.lock:
            return list(self.history)

    def read_output(self, func):
        for line in self.process.stdout:
            with self.lock:
                self.history.append(line)

            func(line)

    def get_memory_usage(self):
        if self.process is None:
            return 0

        process = psutil.Process(self.process.pid)
        memory = process.memory_info().rss
        return memory



# some functions

def add_to_db(id,name,gameType,path,ownerID):
    new_game = GameServer(serverId=id, serverName=name, gameType=gameType, serverPath=path, ownerID=ownerID)
    db.session.add(new_game)
    db.session.commit()



#recursive function to get the size of a directory
def get_dir_size (path):
    total = 0
    for f in os.listdir(path):
        filepath = os.path.join(path,f)
        if os.path.isdir(filepath):
            #recursive case - that its another directory
            total += get_dir_size(filepath)
        else:
            #base case - if its a file we can get the size of that file
            total += os.path.getsize(filepath)
    return total


        



