#!/usr/bin/env python

"""
Start of TCP fuzzing server. Still very rough.
"""

import socket
import select
import signal
import time
import sys
import os
import Queue
import constants as fuzz_constants

BUFSIZ = 1024

# Things to do:
# - Expect abilities. example: client sends PASS*, server sends +OK
# - Use this class to actually build some fuzzers
# - ability to omit \r\n
# - Count fuzz strings

class FuzzTCPServer(object):
    """TCP Server object for thefuzz suite"""

    def __init__(self, bindaddr="0.0.0.0", port=4444, backlog=5):
        self.inputs = []
        self.outputs = []
        self.clientmap = {}
        self.banner = None

        self.fuzz_queue = Queue.Queue()

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

        # Create listen socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)

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


    @staticmethod
    def get_fuzz_strings(string):
        """get_fuzz_strings() -- Parses a line from a script file, returning
                              -- relevant fuzz strings. Ex: @bof@ will return a
                              -- tuple of strings that may trigger buffer
                              -- overflows.

        Args:
            string (str) - String containing a line from a configuration file

        Returns:
            A tuple of tuples containing relevant fuzz strings
        """
        count = 0
        fuzz_strings = ()

        for variable in fuzz_constants.FUZZ_VARS:
            count += 1
            if variable[0] in string:
                fuzz_strings = fuzz_constants.FUZZ_VARS[count - 1][1]
                break

        return fuzz_strings


    def add_script(self, script_file):
        """add_script() -- Parses a script file, adding fuzz items to queue.

        Args:
            script_file (str) - Path to script file.

        Returns:
            True if the file was parsed successfully.
            False if the file was not parsed successfully.
        """
        if not os.access(script_file, os.R_OK):
            print "[-] Could not open %s for reading" % script_file
            return False

        linecount = 0
        for line in open(script_file, "r"):
            linecount += 1
            line = line.rstrip()

            # Skip comments and blank lines
            if line[:1] == "#" or not line:
                continue

            # Make sure only variable per line exists
            varcount = 0
            for var in fuzz_constants.FUZZ_VARS:
                varcount += line.count(var[0])
            if varcount > 1:
                print "[-] Too many variables on line %d of %s. Skipping." % \
                    (linecount, script_file)
                print "    %s\n" % line
                continue

            # Add lines without variables as they are
            if varcount == 0:
                self.fuzz_queue.put(line + "\r\n")
                continue

            # Get fuzz strings based on variable in line
            fuzz_strings = self.get_fuzz_strings(line)

            # Replace variable name with @@
            for variable in fuzz_constants.FUZZ_VARS:
                if variable[0] in line:
                    line = line.replace(variable[0], "@@")
                    break

            # Add fuzz strings to queue
            for fuzz_string in fuzz_strings:
                self.fuzz_queue.put(line.replace("@@", fuzz_string[1]) + "\r\n")

        return True

    def add_connection(self, sock, address):
        """add_connection() -- Adds an incoming connection to inputs and outputs
                            -- lists. This is for internal record keeping.

        Args:
            sock (fd)     - Socket of the incoming connection.
            address (str) - IP address of incoming connection.

        Returns:
            Nothing.
        """
        self.inputs.append(sock)
        self.outputs.append(sock)
        self.clientmap[sock] = address[0]


    def remove_connection(self, sock):
        """remove_connection() -- Removes a connection from internal list.

        Args:
            sock (fd) - Socket that is going away.

        Returns:
            Nothing.
        """
        sock.close()
        self.inputs.remove(sock)
        if sock in self.outputs:
            self.outputs.remove(sock)


    def getname(self, sock):
        """getname() -- Get IP address of a socket.

        Args:
            sock (fd) - Socket fd

        Returns:
            IP address of socket
        """
        return self.clientmap[sock]


    def siginthandler(self, signum, _):
        """siginthandler() -- Handle SIGINT (Control-C, usually). Close sockets
                           -- and exit the program as cleanly as possible.

        Args:
            signum (int) - Signal number.

        Returns:
            Nothing.
        """
        print "[-] Caught signal %d" % signum
        print "[-] Exiting."

        for output in self.outputs:
            output.close()

        self.server.close()


    def send(self, sock, buf):
        """send() -- Sends data to a socket.

        Args:
            sock (fd) - Socket to send data to.
            buf (str) - Data to send to the socket.

        Returns:
            True if send was successful.
            False if send was unsuccessful.
        """
        try:
            sock.send(buf)
        except socket.error, exc:
            print "[-] Failed to send to %s: %s" % (self.getname(sock), exc)
            return False

        return True


    def recv(self, sock, bufsiz):
        """recv() -- Receive data from a socket.

        Args:
            sock (fd)    - Socket to receive data from.
            bufsiz (int) - Number of bytes to read.

        Returns:
            String containing data if there was data to be had.
            None if there was no data or an error occurred
        """
        try:
            data = sock.recv(bufsiz)
            if data:
                return data
            return None
        except socket.error, exc:
            print "[-] Failed to read from %s: %s" % (self.getname(sock), exc)
            return None


    def serve(self, delay=0):
        """serve() -- Main server loop.

        Args:
            delay (int) -- Delay between sending fuzz strings (default: 0)

        Returns:
            True after all fuzz strings have been exhausted.
        """
        self.inputs = [self.server]

        running = True
        while running:
            try:
                inputs, outputs, exceptions = select.select(self.inputs, self.outputs, [])
            except select.error, exc:
                break

            except socket.error, exc:
                break

            # Process inputs from select()
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
                        print "[*] %s: %s" % (self.getname(sock), data.rstrip())
                    else:
                        print "[-] %s Disconnected" % self.getname(sock)
                        self.remove_connection(sock)

            # Process outputs from select()
            for sock in outputs:
                if not self.fuzz_queue.empty():
                    current_fuzz = self.fuzz_queue.get()
                    if self.send(sock, current_fuzz) is False:
                        break

                    time.sleep(delay)
                else:
                    #done!
                    running = False
                    print "[+] Done."

            # Process exceptions from select()
            for sock in exceptions:
                print "[-] exception in %s" % self.getname(sock)
                self.remove_connection(sock)

        self.server.close()
        return True
