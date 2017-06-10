
# Introduction

This is the beginning of a suite of fuzz testing tools. It is not
complete at the moment and almost assuredly contains multiple
bugs. Documentation is also lacking, but will be addressed in the near
future.

# What's included?

## fuzz_cli.py 

This is a CLI program fuzzer. It supports CLI arguments and
environment variables as fuzzing targets.

	$ ./fuzz_cli.py tests/getopt scripts/getopt.fuzz -v

To disable the free() warning in glibc when you trigger a heap
overflow:

	$ MALLOC_CHECK_=0 ./fuzz_cli.py tests/getopt scripts/getopt.fuzz

See scripts/ directory for examples of scripts.

## tests/ld_preload-get-vars.so

This is a library that intercepts the different getopt() functions and
getenv().It displays what flags work on a program and which
environment variables are pulled. This is very useful for making a
fuzzing script to use with fuzz_cli.py.

	$ cd tests
	$ make
	$ LD_PRELOAD="./tests/ld_preload-get-vars.so" /bin/nc.traditional -n
	getopt(abc:e:g:G:hi:klno:p:q:rs:T:tuvw:zC)
	getenv(HOSTALIASES)
	getenv(HOSTALIASES)

So with this output, you know that -c, -e, -g, -G, -i, -o, -p, -q, -s,
-T, and -w take arguments and it uses the HOSTALIASES environment
variable. You can use this knowledge to create a file like so:

nc.fuzz:
```
ENV:HOSTALIASES="@@" asdf
@@
1 @@
1 2 @@
1 2 3 @@
-c @@ asdf
-e @@ asdf
-g @@ asdf
-G @@ asdf
-i @@ asdf
-o @@ asdf
-p @@ asdf
-q @@ asdf
-s @@ asdf
-T @@ asdf
-w @@ asdf
```

## FuzzTCPServer.py

This file contains a class for crafting TCP servers to fuzz
clients. For example, a simple IRC fuzzer:

```
#!/usr/bin/env python

# Example of an IRC fuzzing server

from FuzzTCPServer import *

def main():
    """main function"""
    fuzz = FuzzTCPServer(bindaddr="0.0.0.0", port=6667)
    fuzz.banner = "Welcome to the best irc server ever.\r\n"
    fuzz.add_script("scripts/irc-server.script")
    fuzz.serve(delay=0.01)


if __name__ == "__main__":
    main()

```

This is similar to the CLI fuzzer in the scripting language. Each line
if it contains a variable will be sent to the client with the naughty
strings in place of variables:

```
# Server notices
:compton.deathrow.net NOTICE * :*** Looking up your hostname...
:@@ NOTICE * :*** Looking up your hostname...
:compton.deathrow.net @@ * :*** Looking up your hostname...
:compton.deathrow.net NOTICE @@ :***Looking up your hostname...
:compton.deathrow.net NOTICE * :@@

# CAP reply
:@@ CAP * LS :account-notify extended-join identify-msg multi-prefix sasl
:compton.deathrow.net @@ * LS :account-notify extended-join identify-msg multi-prefix sasl
:compton.deathrow.net CAP @@ LS :account-notify extended-join identify-msg multi-prefix sasl
:compton.deathrow.net CAP * @@ :account-notify extended-join identify-msg multi-prefix sasl
:compton.deathrow.net CAP * LS :@@

# CAP ACK
:@@ CAP TupacSecure  ACK :multi-prefix
:compton.deathrow.net @@ TupacSecure  ACK :multi-prefix
:compton.deathrow.net CAP @@ ACK :multi-prefix
:compton.deathrow.net CAP TupacSecure @@ :multi-prefix
:compton.deathrow.net CAP TupacSecure ACK :@@

# Numeric 001
:@@ 001 TupacSecure :Welcome to the Thug Life
:compton.deathrow.net @@ TupacSecure :Welcome to the Thug Life
:compton.deathrow.net 001 @@ :Welcome to the Thug Life
:compton.deathrow.net 001 TupacSecure :@@

...
...
...
```

