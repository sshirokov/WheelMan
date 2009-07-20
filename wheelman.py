#!/usr/bin/env python
from datetime import datetime
from libs.handler import Handler
from libs.irclib import nm_to_n

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


def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.set_routes(DISPATCH)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

