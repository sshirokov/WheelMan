from wheelman.libs.irclib import nm_to_n
from wheelman.core.fsm.states import Anonymous

class FSM(object):
    def __init__(self):
        self.user_fsm = {}
        self.pending_events = []

    def get_user_states(self, user):
        return self.user_fsm.get(nm_to_n(user), [])

    def update_user_state(self, user, old, new):
        self.user_fsm[nm_to_n(user)].remove(old)
        self.user_fsm[nm_to_n(user)].append(new)

    def add_initial_user_state(self, user, data = None, state=Anonymous):
        if not self.user_fsm.get(nm_to_n(user)):
            self.user_fsm[nm_to_n(user)] = []
        self.user_fsm[nm_to_n(user)].append(state(data))
        return self.get_user_states(user)

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
            if user_state[1] in [type(s) for s in self.get_user_states(user_state[0])]:
                print "%s eligible to fire: %s => %s: %s" % (user_state,
                                                             handler_event[1].source(),
                                                             handler_event[1].target(),
                                                             handler_event[1].arguments())
                print "Removing from pend queue, adding to exec queue"
                self.pending_events.remove((user_state, handler_event))
                to_fire.append(handler_event)
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
        for target in targets:
            states = self.get_user_states(target)
            next_states = [s.transition(event) for s in states]
            for state, next_state in zip(states, next_states):
                if state and next_state:
                    self.update_user_state(target, state, next_state)
                    print "Transitioning[%s] %s => %s" % (target, state, next_state)
        self.fire_and_clear_all()

fsm = FSM()
