from wheelman.libs.wtfsm import make_states, State, Transition
from wheelman.libs.irclib import nm_to_n

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

    def set_user_state(self, user, state):
        self.user_fsm[nm_to_n(user)] = state

    def set_initial_user_state(self, user, data = None):
        self.user_fsm[nm_to_n(user)] = Anonymous(data)
        return self.get_user_state(user)

    def input(self, event):
        print "All FSM:", self.user_fsm
        targets = filter(lambda t: type(t) in (str, unicode),
                         (event.source(),
                          event.target(),
                          len(event.arguments()) and event.arguments()[0]))
        next_state = None
        for target in targets:
            state = self.get_user_state(target)
            next_state = getattr(state, 'transition', lambda e: None)(event)
            if state and next_state:
                self.set_user_state(target, next_state)
                print "Transitioning[%s] %s => %s" % (target, state, next_state)
                break            
        return next_state

fsm = FSM()
