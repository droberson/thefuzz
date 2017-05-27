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

- fuzz_cli.py -- a CLI fuzzer

	$ ./fuzz_cli.py tests/getopt scripts/getopt.fuzz -v

To disable the free() warning in glibc when you trigger a heap overflow:

	$ MALLOC_CHECK_=0 ./fuzz_cli.py tests/getopt scripts/getopt.fuzz

See scripts/ directory for examples of scripts.

