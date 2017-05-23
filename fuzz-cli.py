#!/usr/bin/env python

"""
fuzz.py -- CLI fuzzer
  by Daniel Roberson @dmfroberson

TODO:
- map signal numbers to names
- be verbose when potential errors are encountered
- split up fuzz strings by type: @bof@, @sqli@, @fmtstr@, ...
- add timeout option
- make not so ugly!!
- logging
"""

import os
import sys
import shlex
import subprocess32

# TODO More strings. See fuzzdb project:
#    https://github.com/fuzzdb-project/fuzzdb
FUZZ = [
    ["Single %s",           "%s"],
    ["Eight %s",            "%s" * 8],
    ["Eight %s with space", "%s " * 8],
    ["Zero",                "0"],
    ["Negative 1",          "-1"],
    ["128 bytes",           "A" * 128],
    ["256 bytes",           "A" * 256],
    ["512 bytes",           "A" * 512],
    ["1024 bytes",          "A" * 1024],
    ["4096 bytes",          "A" * 4086],
    ["8192 bytes",          "A" * 8192]
]

FUZZVARS = [
    "@@" # All types
]


def fuzz_test(arguments, timeout=0):
    """
    fuzz_test() -- iterates through fuzz strings, supplying them to the target
                -- program. No return value.
    """
    for fuzz_string in FUZZ:
        # Replace @@ with fuzz string
        current_fuzz = []
        for arg in arguments:
            # TODO add more options: @sqli@, @fmtstr@, @bof@ ...
            if arg == "@@":
                current_fuzz.append(fuzz_string[1])
            current_fuzz.append(arg)

        process = subprocess32.Popen(args=current_fuzz,
                                   shell=False,
                                   stdout=subprocess32.PIPE,
                                   stderr=subprocess32.PIPE)

        out = ""
        err = ""
        try:
            out, err = process.communicate(timeout=timeout)
        except subprocess32.TimeoutExpired:
            process.terminate()

        print " [*] exit:%sstdout:%sstderr:%stest:%s" % \
            (str(process.returncode).ljust(8),
             str(len(out)).ljust(8),
             str(len(err)).ljust(8),
             fuzz_string[0])


if __name__ == "__main__":
    print "[+] fuzz.py -- by Daniel Roberson @dmfroberson"
    print

    if len(sys.argv) != 3:
        print "[-] Not enough arguments!"
        print "[-] usage: ./fuzz.py /path/to/binary /path/to/script"
        print "[-] Exiting."
        exit(os.EX_USAGE)

    # Make sure first argument exists and is executable
    if os.path.isfile(sys.argv[1]) and os.access(sys.argv[1], os.X_OK):
        progname = sys.argv[1]
    else:
        print "[-] Specified program \"%s\" is not executable." % sys.argv[1]
        print "[-] Exiting."
        exit(os.EX_USAGE)

    # Make sure script is readable
    if os.access(sys.argv[2], os.R_OK):
        testfile = sys.argv[2]
    else:
        print "[-] Specified script \"%s\" is not readable." % sys.argv[2]
        print "[-] Exiting."
        exit(os.EX_USAGE)

    print "[+] Fuzzing %s with tests defined in %s" % (progname, testfile)
    print

    linecount = 0
    for line in open(testfile, "r"):
        linecount += 1

        line = line.rstrip()

        # Skip blank lines
        if len(line) == 0:
            continue

        # Skip comments
        if line[:1] == "#":
            continue

        # Make sure only one @@ per line
        varcount = 0
        for variable in FUZZVARS:
            varcount += line.count(variable)
        if varcount > 1:
            print "[-] Too many variables on line %d of %s -- Skipping." % \
                (linecount, testfile)
            print "    %s", line
            print
            continue

        # Create argv[] for Popen()
        args = shlex.split(line)
        args.insert(0, progname)

        # Finally, fuzz the target
        print "[+] %s" % args
        fuzz_test(args, timeout=1)
        print

    # All done.
    print
    print "[+] Pledge your allegiance to Shadaloo and I will let you live!"
    print "[+] Done"
