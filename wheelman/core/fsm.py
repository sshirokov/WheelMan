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
        #What a fucking mess..
        origin = event.source() or event.target() or ""
        state, new_state = self.get_user_state(origin), None
        if not state:
            origin = event.target() or ""
            state = self.get_user_state(origin)
        if state: new_state = state.transition(event)
        if new_state:
            self.set_user_state(origin, new_state)
            print "Transitioning[%s] %s => %s" % (origin,
                                                  state,
                                                  new_state)
        return new_state

fsm = FSM()
