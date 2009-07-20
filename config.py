import os

DEBUG = True

DATABASE="sqlite:///%s/db.db" % os.path.dirname(__file__)
