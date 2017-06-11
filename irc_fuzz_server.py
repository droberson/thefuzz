#!/usr/bin/env python

# Example of an IRC fuzzing server

import sys
from FuzzTCPServer import *

def main():
    """main function"""
    port = 6667
    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    fuzz = FuzzTCPServer(bindaddr="0.0.0.0", port=port)
    fuzz.banner = "Welcome to the best irc server ever.\r\n"
    fuzz.add_script("scripts/irc-server.script")
    fuzz.serve(delay=0.01)


if __name__ == "__main__":
    main()
