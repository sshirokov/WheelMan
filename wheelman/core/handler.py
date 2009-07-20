import re
from wheelman.libs.ircbot import SingleServerIRCBot
from wheelman.libs.irclib import nm_to_n
from wheelman.libs.utils import ObjDict
import wheelman.core.router as router

class Handler(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.routes = ObjDict(dict(router.DISPATCH))

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

    def _reply(self, connection, target, reply):
        connection.privmsg(target, reply)

    def on_privmsg(self, connection, e):
        self._pass_message(connection, e)
        response = self._route_message(connection, e, self.routes.private)
        if response and type(response) in (str, unicode):
            self._reply(connection, nm_to_n(e.source()), response)
        if response and type(response) in (list, tuple):
            map(lambda line: self._reply(connection, nm_to_n(e.source()), line), response)


    def on_pubmsg(self, connection, e):
        self._pass_message(connection, e)
        response = self._route_message(connection, e, self.routes.public)
        if response and type(response) in (str, unicode):
            self._reply(connection, e.target(), response)
        if response and type(response) in (list, tuple):
            map(lambda line: self._reply(connection, e.target(), line), response)

    def _trace_event(self, connection, e):
        print "EventTrace: [%s](%s => %s):" % (e.eventtype(), e.source(), e.target()), e.arguments()
    on_nick = _trace_event
    on_join = _trace_event
    on_part = _trace_event
    on_quit = _trace_event
