#!/usr/bin/env python
print "Loading..."

from datetime import datetime
import re
from libs.ircbot import SingleServerIRCBot
from libs.irclib import nm_to_n

class ObjDict(dict):
    def init(self, d): self.update(d)
    def __getattr__(self, attr): return self[attr]
    def __setattr__(self, attr, val): self[attr] = val

def log_message(meta, message):
    print "Logging: %s=>%s: %s" % (meta.event.source(), meta.event.target(), message)
    


def targetted_public_message(meta, name, message):
    print "%s: Handling message: %s=>%s: %s" % (datetime.now(),
                                              nm_to_n(meta.event.source()),
                                              meta.event.target(),
                                              meta.event.arguments())
    print "Name:", name
    print "Message:", message

def debug_repl(meta):
    import pdb; pdb.set_trace()

DISPATCH = (
    ('public', (
            (r'^(?P<name>[^\s]+):\s{1,}(?P<message>.+)\s*$', targetted_public_message),
    )),
    ('private', (
            (r'^DEBUG::repl\(\)$', debug_repl),
    )),
    ('passive', (
            (r'^(?P<message>.+)$', log_message),
    )),
)

class Handler(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def set_routes(self, routes):
        self.routes = ObjDict(dict(routes))

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
            
        

def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.set_routes(DISPATCH)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

