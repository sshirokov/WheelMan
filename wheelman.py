#!/usr/bin/env python
from datetime import datetime
from wheelman.core.handler import Handler
from wheelman.libs.irclib import nm_to_n

def targetted_public_message(meta, name, message):
    print "%s: Handling message: %s=>%s: %s" % (datetime.now(),
                                              nm_to_n(meta.event.source()),
                                              meta.event.target(),
                                              meta.event.arguments())
    print "Name:", name
    print "Message:", message

def nop(meta):
    print "NOP"

import wheelman.core.router as router
router.add_routes(('',
        ('public', (
                (r'^(?P<name>[^\s]+):\s+(?P<message>.+)\s*$', targetted_public_message),
        )),
        ('passive', (
                (r'^NOP$', nop),
        )),
)) 

def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

