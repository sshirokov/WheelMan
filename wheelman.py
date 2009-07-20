#!/usr/bin/env python
from wheelman.core.handler import Handler

import wheelman.core.router as router
router.add_routes(('handlers',
        ('private', (
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo_verbose'),
        )),
        ('public', (
                (r'^echo:\s+(?P<message>.+)\s*$', 'echo'),
                (r'^(?P<name>[^\s]+):\s+(?P<message>.+)\s*$', 'targetted_public_message'),
        )),
        ('passive', (
                (r'^NOP$', 'nop'),
        )),
)) 

def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

