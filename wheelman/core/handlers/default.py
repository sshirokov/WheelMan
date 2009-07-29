from wheelman.libs.irclib import nm_to_n
from wheelman.core.db import Session

def log_message(meta, message):
    from wheelman.core.models import Log
    print "Logging: %s => %s: %s" % (meta.event.source(), meta.event.target(), message)
    session = Session()
    session.add(Log(type = meta.event.eventtype(),
                    source = nm_to_n(meta.event.source()),
                    target = meta.event.target(),
                    text = message))
    session.commit()
    session.close()
    

def debug_repl(meta):
    import pdb; pdb.set_trace()

def debug_eval(meta, code):
    try: return unicode(eval(code))
    except Exception, e: return "Exception raised: %s" % e

def debug_db_flush(meta):
    session.flush()
    return "Flushed db"

def debug_db_commit(meta):
    session.commit()
    return "Flushed db"

def die(meta, message):
    import sys
    message = message or "I've been asked to leave by %s" % nm_to_n(meta.event.source())
    meta.connection.quit(message)
    sys.exit(0) #TODO: This should be an exception handled at the top
    
def user_returned(meta, user):
    from wheelman.core.models import User, Log
    session = Session()
    reply = ["Welcome back",
             "I missed you!"]
    last_seen = session.query(User.last_seen).filter_by(nick = user).first()
    if not last_seen:
        print "WARNING: User has returned, but we've never seen him before."
        session.close()
        return
    else: last_seen = last_seen[0]
    missed = session.query(Log)\
        .filter_by(target = meta.origin.channel)\
        .filter(Log.type.in_(["pubmsg", "ctcp"]))\
        .filter("created_at > :ls").params(ls = last_seen).all()
    missed = ["%s <%s> %s" % (row.created_at.strftime("%m/%d/%y %I:%M:%S%p"),
                              row.source,
                              row.text)
              for row in missed]
    if len(missed):
        reply += ["You missed some things :("] + missed
    else:
        reply.append("You didn't miss anything!")
    session.close()
    User.see_user(user)
    meta.origin.reply(user, reply)
