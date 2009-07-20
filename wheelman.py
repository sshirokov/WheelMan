#!/usr/bin/env python
from libs.ircbot import SingleServerIRCBot

class TestBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        print "c(%s) e(%e)"

    def on_pubmsg(self, c, e):
        print "c(%s) e(%e)"

def main():
    bot = TestBot("#botworld", "WheelMan", "localhost", 6669)
    bot.start()

if __name__ == "__main__":
    main()

