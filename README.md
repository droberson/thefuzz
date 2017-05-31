                            THE FUZZ!@#$

                          ________________
                          \      __      /         __
                           \_____()_____/         /  )
                           '============`        /  /
                            #---\  /---#        /  /
                           (# @\| |/@  #)      /  /
                            \   (_)   /       /  /
                            |\ '---` /|      /  /
                    _______/ \\_____// \____/ o_|
                   /       \  /     \  /   / o_|
                  / |           o|        / o_| \
                 /  |  _____     |       / /   \ \
                /   |  |===|    o|      / /\    \ \
               |    |   \@/      |     / /  \    \ \
               |    |___________o|__/----)   \    \/
               |    '              ||  --)    \     |
               |___________________||  --)     \    /
                    |           o|   ''''   |   \__/
                    |            |          |

                      "DON'T CROSS ME... !"
    Rosebud


# Introduction

This is the start of some fuzzing tools. Please use this opportunity
to enjoy the savage police officer with a nightstick ASCII art.


# What's included?

- fuzz_cli.py 

This is a CLI program fuzzer. It supports CLI arguments and environment
variables as fuzzing targets.

	$ ./fuzz_cli.py tests/getopt scripts/getopt.fuzz -v

To disable the free() warning in glibc when you trigger a heap overflow:

	$ MALLOC_CHECK_=0 ./fuzz_cli.py tests/getopt scripts/getopt.fuzz

See scripts/ directory for examples of scripts.

- tests/ld_preload-get-vars.so

This is a library that intercepts the different getopt() functions and getenv().It displays what flags work on a program and which environment variables are
pulled. This is very useful for making a fuzzing script to use with fuzz_cli.py.

	$ cd tests
	$ make
	$ LD_PRELOAD="./tests/ld_preload-get-vars.so" /bin/nc.traditional -n
	getopt(abc:e:g:G:hi:klno:p:q:rs:T:tuvw:zC)
	getenv(HOSTALIASES)
	getenv(HOSTALIASES)

So with this output, you know that -c, -e, -g, -G, -i, -o, -p, -q, -s, -T, and
-w take arguments and it uses the HOSTALIASES environment variable. You can use
this knowledge to create a file like so:

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

