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
"""

import subprocess

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

def fuzz_test(arguments):
    for fuzz_string in FUZZ:
        current_fuzz = []
        for arg in arguments:
            if arg == "@@":
                current_fuzz.append(fuzz_string[1])
            current_fuzz.append(arg)
        #process = subprocess.Popen(args=["./tests/fmt", fuzz_string[1]],
        process = subprocess.Popen(args=current_fuzz,
                                   shell=False,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        out, err = process.communicate()

        print "exit:%sstdout:%sstderr:%stest:%s" % \
            (str(process.returncode).ljust(8),
             str(len(out)).ljust(8),
             str(len(err)).ljust(8),
             fuzz_string[0])


if __name__ == "__main__":
    # TODO specify fuzz file
    # TODO getopt/usage stuff
    for line in open("test.fuzz", "r"):
        # Skip blank lines
        if len(line.rstrip()) == 0:
            continue

        # Skip comments
        if line[:1] == "#":
            continue

        # TODO: Make sure first word is executable
        # TODO: Make sure only one @@ per line
        args = line.split()
        fuzz_test(args)
