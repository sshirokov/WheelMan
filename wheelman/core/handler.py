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

    def _route_message(self, connection, event, routes, early = False):
        meta = ObjDict({'origin': self, 'connection': connection, 'event': event})
        for route in routes:
            m = re.compile(route[0]).match(event.arguments()[0])
            if m:
                print "Dispatching to:", route[1]
                response = route[1](meta, **m.groupdict())
                if early: return response
            else: print "Failed to route on:", route[0]

    def _pass_message(self, connection, event):
        return self._route_message(connection, event, self.routes.passive, early=False)

    def on_welcome(self, connection, e):
        connection.join(self.channel)

    def on_privmsg(self, connection, e):
        self._pass_message(connection, e)
        self._route_message(connection, e, self.routes.private)

    def on_pubmsg(self, connection, e):
        self._pass_message(connection, e)
        self._route_message(connection, e, self.routes.public)
