from database import db, User, GameServer
#from game import GameCreator
from sqlalchemy import select
import os

GAME_SERVERS = {}

ROOT_DIR = os.getenv("ROOT_DIR")
GAME_PATH = ROOT_DIR+"/games_tmp/"



