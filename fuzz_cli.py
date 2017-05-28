#!/usr/bin/env python

"""
fuzz_cli.py -- CLI fuzzer
  by Daniel Roberson @dmfroberson

TODO:
- Environment variable support
- Interactive program support (pexpect?)
- Test on different platforms:
  - OpenWRT
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

LOGGING = False
LOGFILE = "fuzz_cli.out"

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


def xprint(buf):
    """xprint() -- wrapper for print function that logs if logging is enabled

    Args:
        buf (str) - String to print/log

    Returns:
        Nothing.
    """
    if LOGGING:
        with open(LOGFILE, "a") as logfile:
            logfile.write(buf + "\n")

    print buf


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
    count = 0
    fuzz_strings = ()
    for variable in fuzz_constants.FUZZ_VARS:
        count += 1
        if any(variable[0] in s for s in arguments):
            arguments = [x.replace(variable[0], "@@") for x in arguments]
            fuzz_strings = fuzz_constants.FUZZ_VARS[count - 1][1]
            break

    if not fuzz_strings:
        xprint("[-] Invalid variable name in arguments: %s" % arguments)
        return

    # Perform the actual fuzzing
    for fuzz_string in fuzz_strings:
        current_fuzz = []
        for arg in arguments:
            if "@@" in arg: # Replace this with string
                current_fuzz.append(arg.replace("@@", fuzz_string[1]))
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
        xprint(" [*] exit:%sstdout:%sstderr:%stime:%.4f   test:%s" % \
            (str(signal_to_human(process.returncode)).ljust(8),
             str(len(out)).ljust(7),
             str(len(err)).ljust(7),
             time_elapsed,
             fuzz_string[0]))

        if verbose is True:
            xprint("  [*] stdout: %s" % out)
            xprint("  [*] stderr: %s" % err)

def parse_cli():
    """parse_cli() -- parses cli input and sets variables accordingly"""
    description = "example: ./fuzz-cli.py [-v] [-t <timeout>] <binary> <script>"
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
    parser.add_argument("-l",
                        "--logfile",
                        required=False,
                        help="Specify logfile to save output.")
    args = parser.parse_args()
    return args


def main():
    """main() function
    """
    global LOGGING
    global LOGFILE
    xprint("[+] fuzz_cli.py -- by Daniel Roberson @dmfroberson\n")

    args = parse_cli()

    # Make sure target exists and is executable
    progname = args.binary[0]
    if not os.path.isfile(progname) and not os.access(progname, os.X_OK):
        xprint("[-] Specified program \"%s\" is not executable." % progname)
        xprint("[-] Exiting.")
        exit(os.EX_USAGE)

    # Make sure script is readable
    scriptfile = args.script[0]
    if not os.access(scriptfile, os.R_OK):
        xprint("[-] Specified script \"%s\" is not readable." % scriptfile)
        xprint("[-] Exiting.")
        exit(os.EX_USAGE)

    # Make sure logfile is writable and set up logging
    if args.logfile:
        LOGFILE = args.logfile
        try:
            logfile = open(LOGFILE, "w+")
        except IOError, err:
            xprint("[-] Could not open logfile for writing: %s" % str(err))
            xprint("[-] Exiting.")
            exit(os.EX_OSFILE)

        logfile.close()
        LOGGING = True

    xprint("[+] Fuzzing %s with tests defined in %s\n" % (progname, scriptfile))

    linecount = 0
    for line in open(scriptfile, "r"):
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
            xprint("[-] Too many variables on line %d of %s -- Skipping." % \
                (linecount, scriptfile))
            xprint("    %s\n" % line)
            continue

        # Create argv[] for Popen()
        fuzz_args = shlex.split(line)
        fuzz_args.insert(0, progname)

        # Finally, fuzz the target
        xprint("[+] Fuzzing: %s" % " ".join(fuzz_args))
        fuzz_test(fuzz_args, timeout=args.timeout, verbose=args.verbose)
        xprint("")

    # All done.
    xprint("[+] Pledge your allegiance to Shadaloo and I will let you live!")
    xprint("[+] Done")


if __name__ == "__main__":
    main()
