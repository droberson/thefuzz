#!/usr/bin/env python

"""
Start of TCP Fuzzer. Still very rough.
"""

import socket
import select
import signal
import time
import constants as fuzz_constants

BUFSIZ = 1024

# Things to do:
# - Some way to take fuzz inputs rather than hard coding things
# - Save place when something causes a client to disconnect, subsequent
#   reconnects will try next item in fuzz_strings
# - Option to disable select(), only allow 1 connection at a time
# - Send method rather than using socket.send()
# - expect abilities. example: client sends PASS*, server sends +OK

class FuzzTCPServer(object):
    """TCP Server object for thefuzz suite"""

    def __init__(self, bindaddr="0.0.0.0", port=4444, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.inputs = []
        self.outputs = []
        self.banner = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # TODO: make sure bindaddr is valid
        self.server.bind((bindaddr, port))

        print "[+] Listening on %s:%d" % (bindaddr, port)
        self.server.listen(backlog)

        signal.signal(signal.SIGINT, self.siginthandler)

    def add_connection(self, sock, address):
        """Add connection"""
        self.clients += 1
        self.inputs.append(sock)
        self.outputs.append(sock)
        self.clientmap[sock] = (address, str(sock.fileno()))

    def remove_connection(self, sock):
        """Cleanup"""
        self.clients -= 1
        sock.close()
        self.inputs.remove(sock)
        self.outputs.remove(sock)
        del self.clientmap[sock]

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

    def serve(self, delay=0):
        """Main server loop"""
        self.inputs = [self.server]

        running = True

        while running:
            try:
                inputready, _, _ = select.select(self.inputs, self.outputs, [])

            except select.error, exc:
                break

            except socket.error, exc:
                break

            for sock in inputready:
                if sock == self.server:
                    client, address = self.server.accept()
                    print "[+] Incoming connection from %s" % address[0]
                    self.add_connection(client, address)

                    # Send a banner if it exists
                    if self.banner:
                        client.send(self.banner)

                else:
                    try:
                        data = sock.recv(BUFSIZ)

                        if data:
                            print "%s: %s" % (self.getname(sock), data)

                        else:
                            print "[-] %s/%d Disconnected" % \
                                (self.getname(sock), sock.fileno())
                            self.remove_connection(sock)

                    except socket.error, exc:
                        print "[-] Exception: %s -- %s" % \
                            (exc, self.getname(sock))
                        self.remove_connection(sock)

            for output in self.outputs:
                for fuzz in fuzz_constants.FUZZ_ALL:
                    #print fuzz[0]
                    # Put things to fuzz here!!
                    output.send(":%s 311 tupac Tupac thuglife compton.deathrow.net * :Tupac Secure\r\n" % fuzz[1])
                    #output.send(":terribleserver: %s TS TS thuglife compton.deathrow.net * :Tupac Secure\r\n" % fuzz[1])
                    time.sleep(delay)

                #done!
                self.remove_connection(output)
                print "[+] Done."

        self.server.close()


def main():
    """main function"""
    fuzz = FuzzTCPServer(port=6667)
    fuzz.banner = "asdfasdf\r\n"
    fuzz.serve(delay=0.01)


if __name__ == "__main__":
    main()
