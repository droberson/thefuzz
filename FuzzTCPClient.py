#!/usr/bin/env python

"""
Start of TCP fuzzing client. Still very rough!!
"""

import socket
import Queue
import os
import sys
import time
import constants as fuzz_constants


class FuzzTCPClient(object):
    """TCP Client object for thefuzz suite"""

    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.fuzz_queue = Queue.Queue()
        self.header = None

        # Validate IP address
        try:
            socket.inet_aton(server)
        except socket.error:
            print "[-] Invalid IP address: %s" % server
            print "[-] Exiting."
            sys.exit(os.EX_USAGE)

        # Validate port number
        if port > 65535 or port < 1:
            print "[-] Invalid port number: %d" % port
            print "[-] Exiting."
            sys.exit(os.EX_USAGE)

        # Create client socket
        self.client = None


    @staticmethod
    def get_fuzz_strings(string):
        count = 0
        fuzz_strings = ()

        for variable in fuzz_constants.FUZZ_VARS:
            count += 1
            if variable[0] in string:
                fuzz_strings = fuzz_constants.FUZZ_VARS[count - 1][1]
                break

        return fuzz_strings

    def add_script(self, script_file):
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

            # Make sure only one variable per line exists
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

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(1) ### had to do this or header gets lost???

        print "[+] Connecting to %s:%d" % (self.server, self.port)
        try:
            self.client.connect((self.server, self.port))
        except socket.error as exc:
            if exc[0] == 115: # Operation in progress
                pass
            else:
                print "[-] connect error: %s" % exc
                return False

        if self.header is not None:
            self.client.send(self.header)
        self.client.setblocking(0)
        return True


    def fuzz(self, delay=0):
        running = True
        current_fuzz = None

        self.connect()

        buf = ""

        while running:
            try:
                buf = self.client.recv(1024).rstrip()
            except socket.error as exc:
                if exc[0] == 11: # Resource temporarily unavailable
                    pass
                elif exc[0] == 111 or exc[0] == 107:
                    # 107 == not connected
                    # 111 == connection refused
                    self.connect()
                    time.sleep(delay)
                    continue
                else:
                    print "recv error: %s" % exc
            finally:
                if buf:
                    print "recv: %s" % buf

            if current_fuzz is None:
                if not self.fuzz_queue.empty():
                    current_fuzz = self.fuzz_queue.get()
                else:
                    print "[+] Done."
                    running = False
                    continue

            try:
                self.client.send(current_fuzz)
            except socket.error as exc:
                if exc[0] == 32: # Broken pipe.. need to recreate socket :(
                    self.client.close()
                    self.connect()
                else:
                    print "[-] send error: %s" % exc

                time.sleep(delay)
                continue

            current_fuzz = None
            time.sleep(delay)
