from wheelman.libs.wtfsm import make_states, State, Transition

# Whois-based states
####################
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


# Presense-based states
#######################
Present, Absent = make_states("Present", "Absent")

Present(
    Transition(lambda e: e.eventtype() == 'part', Absent),
    Transition(lambda e: e.eventtype() == 'quit', Absent),
    Transition(None, Present))

Absent(
    Transition(lambda e: e.eventtype() == 'join', Present),
    Transition(None, Absent))
