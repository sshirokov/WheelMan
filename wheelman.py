#!/usr/bin/env python
from datetime import datetime
from wheelman.core.handler import Handler
from wheelman.libs.irclib import nm_to_n
import wheelman.core.router as router

def targetted_public_message(meta, name, message):
    print "%s: Handling message: %s=>%s: %s" % (datetime.now(),
                                              nm_to_n(meta.event.source()),
                                              meta.event.target(),
                                              meta.event.arguments())
    print "Name:", name
    print "Message:", message

def debug_repl(meta):
    import pdb; pdb.set_trace()

    

def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.set_routes(router.DEFAULT_DISPATCH)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

