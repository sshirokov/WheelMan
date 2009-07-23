from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime

Base = declarative_base()
class Log(Base):
    __tablename__ = "wheelman_log"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    type = Column(String)
    source = Column(String)
    target = Column(String)
    text = Column(Text)

    def __init__(self, type, source, target, text):
        self.created_at = datetime.now()
        self.type = type
        self.source = source
        self.target = target
        self.text = text

    def __repr__(self):
        return "<Log: %s=>%s: %s...>" % (self.source, self.target, self.text[:10])
