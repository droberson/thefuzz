#!/usr/bin/env python

"""
Start of TCP Fuzzer. Still very rough.
"""

import socket
import select
import signal
import sys
import constants as fuzz_constants

BUFSIZ = 1024

class FuzzTCPServer(object):
    """TCP Server object for thefuzz suite"""

    def __init__(self, bindaddr="0.0.0.0", port=4444, backlog=5):
        self.clients = 0
        self.clientmap = {}

        self.outputs = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((bindaddr, port))

        print "[+] Listening on %s:%d" % (bindaddr, port)
        self.server.listen(backlog)

        signal.signal(signal.SIGINT, self.siginthandler)

    def siginthandler(self, signum, frame):
        """Handle SIGINT"""
        print "[-] Caught Interrupt"

        for output in self.outputs:
            output.close()

        self.server.close()

    def getname(self, client):
        """Get name of client"""
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def serve(self):
        """Main server loop"""
        inputs = [self.server]

        running = True

        while running:
            try:
                inputready, _, _ = select.select(inputs, self.outputs, [])

            except select.error, exc:
                break

            except socket.error, exc:
                break

            for input in inputready:
                if input == self.server:
                    client, address = self.server.accept()
                    print "[+] Incoming connection %d from %s" % \
                        (client.fileno(), address)
                    self.clients += 1
                    inputs.append(client)
                    self.outputs.append(client)
                    self.clientmap[client] = (address, str(client.fileno()))

                # elif input == sys.stdin:
                #     cli_input = sys.stdin.readline()
                #     if cli_input == "/quit\n":
                #         running = False

                else:
                    try:
                        data = input.recv(BUFSIZ)

                        if data:
                            print "%s: %s" % (self.getname(input), data)

                        else:
                            print "[-] %d disconnected" % input.fileno()
                            self.clients -= 1
                            input.close()
                            inputs.remove(input)
                            self.outputs.remove(input)

                    except socket.error, exc:
                        print "[-] Exception: %s -- %s" % (exc, self.getname(input))
                        inputs.remove(input)
                        self.outputs.remove(input)
                        
            for output in self.outputs:
                for fuzz in fuzz_constants.FUZZ_ALL:
                    #print fuzz[1]
                    output.send(":%s 311 tupac Tupac thuglife compton.deathrow.net * :Tupac Secure\r\n" % fuzz[1])
                    output.send(":terribleserver: %s TS TS thuglife compton.deathrow.net * :Tupac Secure\r\n" % fuzz[1]);

                #done!
                print "[+] Done."
                self.outputs.remove(output)
                inputs.remove(output)
                output.close()

        self.server.close()

if __name__ == "__main__":

    Fuzz = FuzzTCPServer(port=6667)
    Fuzz.serve()
