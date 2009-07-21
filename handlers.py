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

#################################################
## FSM BULLSHIT
#################################################
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

class FSM(object):
    def __init__(self):
        self.user_fsm = {}

    def get_user_state(self, user):
        return self.user_fsm.get(nm_to_n(user), None)

    def set_initial_user_state(self, user, data = None):
        self.user_fsm[nm_to_n(user)] = Anonymous(data)
        return self.get_user_state(user)

fsm = FSM()

def need_user_state(state):
    def _d_closure(func):
        def wrapped_func(meta, *args, **kwargs):
            print "wrapped in need_user_state(%s)" % state
            
            user_state = (fsm.get_user_state(meta.event.source()) or
                          fsm.set_initial_user_state(meta.event.source(), data=meta.event))

            print "User state:", user_state,
            
            if type(user_state) == state:
                print "Passing"
                return func(meta, *args, **kwargs)
            else:
                print "Failing"
                return None
            
        return wrapped_func
    return _d_closure

@need_user_state(Registered)
def admin(meta):
    return "Admin action ran"
