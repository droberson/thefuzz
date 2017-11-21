#!/usr/bin/env python

import FuzzTCPClient as dummy

client = dummy.FuzzTCPClient("127.0.0.1", 4444)
client.header = "lololol\r\n"
client.add_script("scripts/dummy.fuzz")
client.fuzz(delay=1)
