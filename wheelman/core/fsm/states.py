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
