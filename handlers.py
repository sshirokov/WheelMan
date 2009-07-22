from datetime import datetime
from wheelman.libs.irclib import nm_to_n
from wheelman.core.fsm.states import Registered
from wheelman.core.decorators import need_user_state


def targetted_public_message(meta, name, message):
    print "%s: Handling message: %s=>%s: %s" % (datetime.now(),
                                              nm_to_n(meta.event.source()),
                                              meta.event.target(),
                                              meta.event.arguments())
    print "Name:", name
    print "Message:", message

def nop(meta): pass

def echo(meta, message):
    return message

def echo_verbose(meta, message):
    return ("Message is %d chars" % len(message),
            message)

@need_user_state(Registered)
def admin(meta):
    return "Admin action ran"
