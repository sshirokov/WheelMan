from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class Log(Base):
    __tablename__ = "wheelman_user"

    id = Column(Integer, primary_key=True)
    nick = Column(String)
    last_seen = Column(DateTime)
    
    def __init__(self, nick):
        self.nick = nick

    def __repr__(self):
        return "<User: %s>" % self.nick
