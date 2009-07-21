class State(object):
    transitions = []

    def __init__(self, *transitions_or_data):
        if len(transitions_or_data) and reduce(lambda acc, e: acc and type(e) == Transition, transitions_or_data, True):
              type(self).transitions = transitions_or_data
        else:
            self.data = {
                1: lambda: transitions_or_data[0],
                0: lambda: None,
            }.get(len(transitions_or_data), lambda: transitions_or_data)()

    def transition(self, data):
        transition = reduce(lambda acc, transition: \
                                acc or (transition.is_valid(data) and transition),
                            self.transitions,
                            None)
        if transition:
            self.data = transition.callback(self.data)
            return transition.next(data)(self.data)
        return None

class Transition(object):
    def __init__(self, test, next_state, callback = lambda data: data):
        self.test = test
        self.next_state = next_state
        self.callback = callback

    def is_valid(self, data):
        if not self.test: return True
        return self.test(data)

    def next(self, data):
        return self.next_state

    def __repr__(self):
        return "<Transition(%s%s )>" % ((self.test and " ") or " Default, ", self.next_state)

def make_states(*names):
    return map(lambda name: type(name, (State,), {}), names)
