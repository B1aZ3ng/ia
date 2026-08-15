from database import db, User, GameServer
from hashlib import sha1
from sqlalchemy import select

asd = GameServer(serverName = "test", gameType = "Minecraft", serverPath = "server_tst/",ownerId = 67)
db.session.add(asd)
db.session.commit()

