#!/usr/bin/env python

fuzz = [
    "%s",
    "%s" * 8,
    "%s " * 8,
    "0",
    "-1",
    "A" * 128,
    "A" * 256,
    "A" * 512,
    "A" * 1024,
    "A" * 4086,
    "A" * 8192
]

import subprocess

for i in fuzz:
    process = subprocess.Popen(args=["./tests/fmt", i],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()

    print "exit:%sout:%serr:%s" % \
        (str(process.returncode).ljust(8), str(len(out)).ljust(8), len(err))
