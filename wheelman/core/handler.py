import re
from wheelman.libs.ircbot import SingleServerIRCBot
from wheelman.libs.irclib import nm_to_n
from wheelman.libs.utils import ObjDict
import wheelman.core.router as router
from wheelman.core.fsm import fsm
from wheelman.core.db import Session
from wheelman.core.models import User
    
class Handler(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.routes = ObjDict(dict(router.DISPATCH))

    def _dispatcher(self, connection, event):
        if event.eventtype() != 'all_raw_messages':
            fsm.input(event)
            print "FSM fed: [%s] %s => %s" % (event.eventtype(), event.source(), event.target())
        super(Handler, self)._dispatcher(connection, event)

    def _route_message(self, connection, event, routes, early = True):
        meta = ObjDict({'origin': self, 'connection': connection, 'event': event})
        for route in routes:
            m = re.compile(route[0]).match(event.arguments()[-1])
            if m:
                print "Dispatching to:", route[1]
                response = route[1](meta, **m.groupdict())
                if early: return response
            else: print "Failed to route on:", route[0]

    def _pass_message(self, connection, event):
        return self._route_message(connection, event, self.routes.passive, early=False)

    def on_welcome(self, connection, e):
        connection.join(self.channel)

    def get_version(self):
        return "WheelMan -- a scriptable bot by Yaroslav Shirokov <slava@hackinggibsons.com>"

    def on_ctcp(self, connection, e):
        if e.arguments()[0] == 'ACTION':
            self._pass_message(connection, e)
            self._route_message(connection, e, self.routes.private)
        else:
            super(Handler, self).on_ctcp(connection, e)

    def _reply(self, target, reply):
        self.connection.privmsg(target, reply)

    def on_privmsg(self, connection, e):
        self._pass_message(connection, e)
        response = self._route_message(connection, e, self.routes.private)
        if response and type(response) in (str, unicode):
            self._reply(nm_to_n(e.source()), response)
        if response and type(response) in (list, tuple):
            map(lambda line: self._reply(nm_to_n(e.source()), line), response)


    def on_pubmsg(self, connection, e):
        self._pass_message(connection, e)
        response = self._route_message(connection, e, self.routes.public)
        if response and type(response) in (str, unicode):
            self._reply(e.target(), response)
        if response and type(response) in (list, tuple):
            map(lambda line: self._reply(e.target(), line), response)

    def on_endofnames(self, connection, e):
        from wheelman.core.fsm import fsm
        from wheelman.core.fsm.states import Present, Absent
        print "NamReply: [%s](%s => %s):" % (e.eventtype(), e.source(), e.target()), e.arguments()
        print "Getting names"
        print "I am in:", self.channel
        print "I know about:", self.channels
        seen = []
        for user in [n for n in self.channels[self.channel].users() if n != self._nickname]:
            print "Seeing user, adding state: %s => %s" % (user, Present)
            User.see_user(user)
            fsm.add_initial_user_state(user, state=Present)
            seen.append(user)
        for user in Session().query(User).filter(~User.nick.in_(seen)).all():
            fsm.add_initial_user_state(user.nick, state=Absent)
            
        from wheelman.core.handlers.default import user_returned
        meta = ObjDict({'origin': self, 'connection': connection, 'event': None})
        fsm.on_transition(Absent, Present, lambda user: user_returned(meta, user))
            
    def _trace_event(self, connection, e):
        print "EventTrace: [%s](%s => %s):" % (e.eventtype(), e.source(), e.target()), e.arguments()
    on_nick = _trace_event
    on_part = _trace_event
    on_quit = _trace_event
    on_notice = _trace_event
