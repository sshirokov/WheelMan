#!/usr/bin/env python
from wheelman.core.handler import Handler
import routes

def main():
    bot = Handler("#botworld", "WheelMan", "localhost", 6669)
    bot.start()

if __name__ == "__main__":
    print "Starting...."
    main()

