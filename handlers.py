from datetime import datetime
from wheelman.libs.irclib import nm_to_n

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

from wheelman.libs.wtfsm import make_states, State, Transition
Anonymous, WhoisWait, Registered = make_states("Anonymous",
                                               "WhoisWait",
                                               "Registered")

Anonymous(
    Transition(lambda e: e.eventtype() == "whoisuser", WhoisWait),
    Transition(None, Anonymous))

WhoisWait(
    Transition(lambda e: e.eventtype() == "registered", Registered),
    Transition(lambda e: e.eventtype() == "endofwhois", Anonymous),
    Transition(None, WhoisWait))

Registered(
    Transition(None, Registered))

fsms = {}

def need_user_state(state):
    pass

@need_user_state(Registered)
def admin(meta):
    return "Admin action ran"
