from wheelman.core.fsm import fsm, Anonymous
from wheelman.libs.irclib import nm_to_n

def need_user_state(state):
    def _d_closure(func):
        def wrapped_func(meta, *args, **kwargs):
            print "wrapped in need_user_state(%s)" % state
            
            user_states = (fsm.get_user_states(meta.event.source()) or
                          [fsm.add_initial_user_state(meta.event.source(),
                                                      state=Anonymous,
                                                      data=meta.event)])

            print "User states:", user_states,
            
            if state in [type(s) for s in user_states]:
                print "Passing"
                return func(meta, *args, **kwargs)
            else:
                print "Failing, and deferring"
                fsm.fire_on((meta.event.source(), state),
                            meta.origin, meta.event)
                meta.connection.whois([nm_to_n(meta.event.source())])
                return None
            
        return wrapped_func
    return _d_closure
