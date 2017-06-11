# TODO

Here's a list of things I'd like to do and some general brainstorming.

## General
- Add globbing, keywords, sqli, files, users, command injections to constants.
- @fast@ -- test most common crashes rather than all

## CLI Fuzzer
- General code cleanup
- Add count to Fuzzing: line
- Timeout override for testing sleep() for sqli and command injections

## HTTP-specific fuzzer
- Since HTTP is so common, a dedicated program for it may be in order.

## TCP Server
- binary!!
- Perhaps it might be a good idea to implement common protocols as their
own tools and have a generic scripting lang for non-common/custom protocols.

## TCP Client
- Start this. Connects to a server as a client and blasts server with data.
- Figure out how to define protocols in script form
- Plaintext and binary!!

## UDP Server
- Start this. See TCP server. Same thing but UDP.

## UDP Client
- Start this. See TCP Client. Same thing but UDP

## Interactive program fuzzer
- For interactive programs/services (nslookup, ftp, ...)
- Need to figure out how to do this over network too (for things like crappy
  Telnet interfaces)
- Figure out a way to define tests

## File-based fuzzer
- Take a config file or whatever the program uses as a template
- Apply targeted mutations
- Run the program over and over with mutated files.

## Lower level/different network protocols
- Use this to test weird IoT devices network stacks
- Ability to apply strange/invalid flags and fields in protocols
- Scapy?? Something else?
- Figure out how to define this in script form
