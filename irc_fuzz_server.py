#!/usr/bin/env python

# Example of an IRC fuzzing server

from FuzzTCPServer import *

def main():
    """main function"""
    fuzz = FuzzTCPServer(bindaddr="0.0.0.0", port=6667)
    fuzz.banner = "Welcome to the best irc server ever.\r\n"
    fuzz.add_script("scripts/irc-server.script")
    fuzz.serve(delay=0.01)


if __name__ == "__main__":
    main()
