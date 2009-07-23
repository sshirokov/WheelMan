import os

DEBUG = True

SERVER_HOST = 'localhost'
SERVER_PORT = 6669
NICK = "WheelMan"
CHANNEL = "#botworld"

DATABASE="sqlite:///%s/db.db" % os.path.dirname(__file__)
