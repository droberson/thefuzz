#!/usr/bin/env python

"""
Example of an IRC fuzzing server using FuzzTCPServer
"""

import sys
import argparse
import FuzzTCPServer as ircfuzz

def main():
    """main function"""
    description = "example: ./irc_fuzz_server.py [-p port] [-b addr] [-d delay]"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p",
                        "--port",
                        default=6667,
                        required=False,
                        help="Port to listen on. Default 6667")
    parser.add_argument("-b",
                        "--bindaddr",
                        default="0.0.0.0",
                        required=False,
                        help="Address to bind to. Default 0.0.0.0")
    parser.add_argument("-d",
                        "--delay",
                        default=0.001,
                        required=False,
                        help="Delay between sending strings. Default 0.001")
    args = parser.parse_args()

    fuzz = ircfuzz.FuzzTCPServer(bindaddr=args.bindaddr, port=args.port)
    fuzz.banner = "Welcome to the best irc server ever.\r\n"
    fuzz.add_script("scripts/irc-server.script")
    fuzz.serve(delay=args.delay)


if __name__ == "__main__":
    main()
