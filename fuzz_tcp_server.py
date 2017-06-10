#!/usr/bin/env python

"""
Start of TCP Fuzzer. Still very rough.
"""

import socket
import select
import signal
import time
import sys
import os
import constants as fuzz_constants

BUFSIZ = 1024

# Things to do:
# - Some way to take fuzz inputs rather than hard coding things
# - Save place when something causes a client to disconnect, subsequent
#   reconnects will try next item in fuzz_strings
# - Option to disable select(), only allow 1 connection at a time
# - expect abilities. example: client sends PASS*, server sends +OK
# - Docstrings

class FuzzTCPServer(object):
    """TCP Server object for thefuzz suite"""

    def __init__(self, bindaddr="0.0.0.0", port=4444, backlog=5):
        self.inputs = []
        self.outputs = []
        self.clientmap = {}
        self.banner = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Validate IP address
        try:
            socket.inet_aton(bindaddr)
        except socket.error:
            print "[-] Invalid bindaddr: %s" % bindaddr
            print "[-] Exiting."
            sys.exit(os.EX_USAGE)

        # Validate port number
        if port > 65535 or port < 1:
            print "[-] Invalid port number: %d" % port
            print "[-] Exiting."
            sys.exit(os.EX_USAGE)

        # bind to port
        try:
            self.server.bind((bindaddr, port))
        except socket.error, exp:
            print "[-] Unable to bind to %s:%d: %s" % (bindaddr, port, exp)
            print "[-] Exiting."
            sys.exit(os.EX_USAGE)

        print "[+] Listening on %s:%d" % (bindaddr, port)
        self.server.listen(backlog)

        signal.signal(signal.SIGINT, self.siginthandler)


    def add_connection(self, sock, address):
        """Add connection"""
        self.inputs.append(sock)
        self.outputs.append(sock)
        self.clientmap[sock] = address[0]


    def remove_connection(self, sock):
        """Cleanup"""
        sock.close()
        self.inputs.remove(sock)
        if sock in self.outputs:
            self.outputs.remove(sock)

    def getname(self, sock):
        """Get hostname"""
        return self.clientmap[sock]

    def siginthandler(self, signum, frame):
        """Handle SIGINT"""
        print "[-] Caught signal %d" % signum
        print "[-] Exiting."

        for output in self.outputs:
            output.close()

        self.server.close()


    def send(self, sock, buf):
        """send data"""
        try:
            sock.send(buf)
        except socket.error, exc:
            print "[-] Failed to send to %s: %s" % (self.getname(sock), exc)
            return False

        return True


    def recv(self, sock, bufsiz):
        """receive data"""
        try:
            data = sock.recv(bufsiz)
            if data:
                return data
            return None
        except socket.error, exc:
            print "[-] Failed to read from %s: %s" % (self.getname(sock), exc)
            return None


    def serve(self, delay=0):
        """Main server loop"""
        self.inputs = [self.server]

        while self.inputs:
            try:
                inputs, outputs, exceptions = select.select(self.inputs, self.outputs, [])
            except select.error, exc:
                break

            for sock in inputs:
                if sock == self.server:
                    client, address = self.server.accept()
                    self.add_connection(client, address)
                    print "[+] Incoming connection from %s" % address[0]

                    # Send a banner if it exists
                    if self.banner:
                        self.send(client, self.banner)

                else:
                    data = self.recv(sock, BUFSIZ)
                    if data:
                        print "%s: %s" % (sock.peername(), data)
                    else:
                        print "[-] %s Disconnected" % self.getname(sock)
                        self.remove_connection(sock)

            for sock in outputs:
                for fuzz in fuzz_constants.FUZZ_ALL:
                    # Put things to fuzz here!!
                    if self.send(sock, ":%s 311 tupac Tupac thuglife compton.deathrow.net * :Tupac Secure\r\n" % fuzz[1]) is False:
                        break

                    time.sleep(delay)

                #done!
                print "[+] Done."

            for sock in exceptions:
                print "[-] exception in %s" % self.getname(sock)
                self.remove_connection(sock)

        self.server.close()


def main():
    """main function"""
    fuzz = FuzzTCPServer(bindaddr="0.0.0.0", port=6667)
    fuzz.banner = "asdfasdf\r\n"
    fuzz.serve(delay=0.01)


if __name__ == "__main__":
    main()
