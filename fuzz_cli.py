#!/usr/bin/env python

"""
fuzz_cli.py -- CLI fuzzer
  by Daniel Roberson @dmfroberson

TODO:
- Environment variable support
- Interactive program support (pexpect?)
- Test on different platforms:
  - OSX
  - FreeBSD
  - RPi
  - OpenWRT
- Logging
- More fuzz strings
  - Common filenames
  - Usernames
  - Directory traversals
  - Command injection
  - Globbing
"""

import os
import time
import shlex
import signal
import argparse
import subprocess32

import constants as fuzz_constants


def signal_to_human(value):
    """signal_to_human() -- provide signal name based on subprocess return code

    Args:
        value (int) - Popen.returncode

    Returns:
        Signal name if it exists, otherwise the original value provided
    """
    signals = {getattr(signal, name) * -1 : name for name in dir(signal) if name.startswith("SIG")}

    if value < 0 and value in signals:
        return signals[value]

    return value


def fuzz_test(arguments, timeout=0, verbose=0):
    """fuzz_test() -- fuzz tests a program with specified types of strings

    Args:
        arguments (list) - list of argments to run against the program. Expects
                           at least one variable in @@ format. See scripts
                           directory for examples.
        timeout (int)    - Timeout in seconds to allow a program to run. A value
                           of 0 disables the timeout, so the programs must exit
                           on their own or be closed by the user.
        verbose (int)    - Toggle verbose output. A value of 1 will output
                           extra data.

    Returns:
        Nothing.
    """
    # Determine what type of fuzz to be performed, based on variable type
    fuzz = []
    for arg in arguments:
        if arg[:1] == "@":
            count = 0
            for variable in fuzz_constants.FUZZ_VARS:
                count += 1
                if arg == variable[0]:
                    fuzz_strings = fuzz_constants.FUZZ_VARS[count - 1][1]
                    fuzz.append("@@")
                    continue

        # Add non-variable CLI argument
        fuzz.append(arg)

    # Perform the actual fuzzing
    for fuzz_string in fuzz_strings:
        current_fuzz = []
        for arg in arguments:
            if arg == "@@": # Replace this with string
                current_fuzz.append(fuzz_string[1])
            else:
                current_fuzz.append(arg)

        process = subprocess32.Popen(args=current_fuzz,
                                     shell=False,
                                     stdout=subprocess32.PIPE,
                                     stderr=subprocess32.PIPE)

        out = ""
        err = ""
        time_start = time.time()

        try:
            out, err = process.communicate(timeout=timeout)
        except subprocess32.TimeoutExpired:
            process.terminate()

        # Display summary of fuzzing run
        time_elapsed = time.time() - time_start
        print " [*] exit:%sstdout:%sstderr:%stime:%.4f   test:%s" % \
            (str(signal_to_human(process.returncode)).ljust(8),
             str(len(out)).ljust(7),
             str(len(err)).ljust(7),
             time_elapsed,
             fuzz_string[0])

        if verbose is True:
            print "  [*] stdout: %s" % out
            print "  [*] stderr: %s" % err


def main():
    """main() function
    """
    print "[+] fuzz_cli.py -- by Daniel Roberson @dmfroberson\n"

    # Parse CLI arguments
    description = "example: ./fuzz_cli.py [-v] [-t <timeout>] <binary> <script>"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("binary",
                        nargs="+",
                        help="Path to binary to fuzz")
    parser.add_argument("script",
                        nargs="+",
                        help="Path to script file containing test cases")
    parser.add_argument("-t",
                        "--timeout",
                        default=1,
                        type=float,
                        required=False,
                        help="Timeout before killing program being fuzzed")
    parser.add_argument("-v",
                        "--verbose",
                        required=False,
                        action="store_true",
                        help="Toggle verbose output")
    args = parser.parse_args()

    # Make sure target exists and is executable
    progname = args.binary[0]
    if not os.path.isfile(progname) and not os.access(progname, os.X_OK):
        print "[-] Specified program \"%s\" is not executable." % progname
        print "[-] Exiting."
        exit(os.EX_USAGE)

    # Make sure script is readable
    testfile = args.script[0]
    if not os.access(testfile, os.R_OK):
        print "[-] Specified script \"%s\" is not readable." % testfile
        print "[-] Exiting."
        exit(os.EX_USAGE)

    print "[+] Fuzzing %s with tests defined in %s\n" % (progname, testfile)

    linecount = 0
    for line in open(testfile, "r"):
        linecount += 1
        line = line.rstrip()

        # Skip comments and blank lines
        if line[:1] == "#" or not line:
            continue

        # Make sure only one @@ per line
        varcount = 0
        for var in fuzz_constants.FUZZ_VARS:
            varcount += line.count(var[0])
        if varcount > 1:
            print "[-] Too many variables on line %d of %s -- Skipping." % \
                (linecount, testfile)
            print "    %s\n" % line
            continue

        # Create argv[] for Popen()
        fuzz_args = shlex.split(line)
        fuzz_args.insert(0, progname)

        # Finally, fuzz the target
        print "[+] Fuzzing: %s" % " ".join(fuzz_args)
        fuzz_test(fuzz_args, timeout=args.timeout, verbose=args.verbose)
        print

    # All done.
    print "[+] Pledge your allegiance to Shadaloo and I will let you live!"
    print "[+] Done"


if __name__ == "__main__":
    main()
