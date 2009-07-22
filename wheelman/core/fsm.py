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
        self.pending_events = []

    def get_user_state(self, user):
        return self.user_fsm.get(nm_to_n(user), None)

    def set_user_state(self, user, state):
        self.user_fsm[nm_to_n(user)] = state

    def set_initial_user_state(self, user, data = None):
        self.user_fsm[nm_to_n(user)] = Anonymous(data)
        return self.get_user_state(user)

    def fire_on(self, target_state, handler, event):
        print "Registering callback on: %s for (%s => %s: %s)" % (target_state,
                                                                  nm_to_n(event.source()),
                                                                  event.target(),
                                                                  event.arguments())
        target, state = nm_to_n(target_state[0]), target_state[1]
        self.pending_events.append( ((target, state), (handler, event)) )

    def fire_and_clear_all(self):
        print "Firing all needed callbacks"
        to_fire = []
        for user_state, handler_event in self.pending_events[:]:
            if user_state[1] == type(self.get_user_state(user_state[0])):
                print "%s eligible to fire: %s => %s: %s" % (user_state,
                                                             handler_event[1].source(),
                                                             handler_event[1].target(),
                                                             handler_event[1].arguments())
                print "Removing from pend queue, adding to exec queue"
                self.pending_events.remove((user_state, handler_event))
                to_fire.append(handler_event)
            else:
                print user_state[1], "==", type(self.get_user_state(user_state[0]))
                print "%s INELIGIBLE to fire: %s => %s: %s" % (user_state,
                                                               handler_event[1].source(),
                                                               handler_event[1].target(),
                                                               handler_event[1].arguments())
        print "Pending triggers remaining:", self.pending_events
        print "Firing all exec queue events"
        map(lambda h_e: h_e[0]._dispatcher(h_e[0].connection, h_e[1]),
            to_fire)

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
        self.fire_and_clear_all()
        return next_state

fsm = FSM()
