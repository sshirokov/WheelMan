from datetime import datetime
from wheelman.libs.irclib import nm_to_n
from wheelman.core.fsm.states import Registered
from wheelman.core.decorators import need_user_state

def nop(meta): pass

def echo(meta, message):
    return message

def echo_verbose(meta, message):
    return ("Message is %d chars" % len(message),
            message)

def dance(meta):
    return ("Just for you, %s" % nm_to_n(meta.event.source()),
            "(^'-')^",
            "(^'-')>",
            "(>'-')>",
            "<('-'^)",
            "^('-'^)",
            "(^'-')^",
            "(^'-')>",
            "(>'-')>",
            "<('-'^)",
            "^('-'^)")

def first_post(meta):
    from wheelman.core.db import Session
    from wheelman.core.models import Log
    who = "Do you think this is a game?"
    session = Session()
    now = datetime.now()
    today = datetime(year=now.year, month=now.month, day=now.day)
    first_log = session.query(Log)\
        .filter(Log.type.in_(["pubmsg", "ctcp"]))\
        .filter("created_at >= :today").params(today = today)\
        .order_by(Log.created_at.asc()).first()
    if first_log: who = "%s is on first." % first_log.source
    session.close()
    return who

@need_user_state(Registered)
def admin(meta):
    return "Admin action ran"
