#!/usr/bin/env python
from wheelman.core.handler import Handler
import wheelman.settings as settings
import routes

def main():
    bot = Handler(settings.CHANNEL,
                  settings.NICK,
                  settings.SERVER_HOST,
                  settings.SERVER_PORT)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

