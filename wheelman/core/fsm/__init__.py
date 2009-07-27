from wheelman.libs.irclib import nm_to_n
from wheelman.core.fsm.states import Anonymous

class FSM(object):
    def __init__(self):
        self.user_fsm = {}
        self.pending_events = []
        self.transition_triggers = []

    def update_nick(self, old, new):
        if self.user_fsm.has_key(old): self.user_fsm[new] = self.user_fsm.pop(old)

        def update_transition_trigger(trigger):
            if trigger[0] == None: return trigger
            return tuple([new] + trigger[1:])
        print "Mapping transition triggers:", self.transition_triggers
        self.transition_triggers = map(update_transition_trigger,
                                       self.transition_triggers)
        print "Done:", self.transition_triggers
        

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

    def on_transition(self, old, new, action, user = None):
        self.transition_triggers.append((user, old, new, action))

    def fire_on_transition(self, user, old, new):
        user = nm_to_n(user)
        print "Searching to fire on: (%s) %s => %s:" % (user, old, new)
        print "Queue:", self.transition_triggers
        for trigger in self.transition_triggers:
            t_user, t_old, t_new, t_action = trigger
            if ((t_user == None) or (t_user == user)) and (t_old == type(old) and t_new == type(new)):
                print "Should fire:", trigger
                t_action(user = user)
                

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
                    self.fire_on_transition(target, state, next_state)
        self.fire_and_clear_all()

fsm = FSM()
