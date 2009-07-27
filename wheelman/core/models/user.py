from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from wheelman.core.db import Session

Base = declarative_base()
class User(Base):
    __tablename__ = "wheelman_user"

    id = Column(Integer, primary_key=True)
    nick = Column(String)
    last_seen = Column(DateTime)
    
    def __init__(self, nick):
        self.nick = nick

    def __repr__(self):
        return "<User: %s>" % self.nick

    @classmethod
    def see_user(self, user):
        session = Session()
        user = session.query(self).filter_by(nick = user).first() or self(user)
        user.last_seen = datetime.now()
        session.merge(user)
        session.commit()
        return user
        
