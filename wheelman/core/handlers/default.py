from wheelman.libs.irclib import nm_to_n
from wheelman.core.db import session

def log_message(meta, message):
    from wheelman.core.models import Log
    print "Logging: %s => %s: %s" % (meta.event.source(), meta.event.target(), message)
    session.add(Log(type = meta.event.eventtype(),
                    source = nm_to_n(meta.event.source()),
                    target = meta.event.target(),
                    text = message))
    session.commit()
    

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
    
