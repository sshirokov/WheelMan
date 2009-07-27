from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import wheelman.settings as settings

engine = create_engine(settings.DATABASE, echo=False, pool_recycle=3600)
Session = sessionmaker(bind=engine)
