#!/usr/bin/env python

"""
fuzz.py -- CLI fuzzer
  by Daniel Roberson @dmfroberson

TODO:
- figure out "scripting language"
- more fuzz strings
- map signal numbers to names
- be verbose when potential errors are encountered
- split up fuzz strings by type: @bof@, @sqli@, @fmtstr@, ...
- add timeout option
"""

import subprocess

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

for i in FUZZ:
    process = subprocess.Popen(args=["./tests/sleep", i[1]],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()

    print "exit:%sstdout:%sstderr:%stest:%s" % \
        (str(process.returncode).ljust(8),
         str(len(out)).ljust(8),
         str(len(err)).ljust(8),
         i[0])
