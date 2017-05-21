# Abstract

Exit value will be 128 + signal when a program exits due to a
signal. When programs crash, they are typically sent a signal on nix
systems. Take the following samples:

- Format string bug
```
% cat fmt.c
#include <stdio.h>

int main(int argc, char *argv[]) {
  printf (argv[1]);
  return 0;
}

% gcc -o fmt fmt.c
fmt.c: In function ‘main’:
fmt.c:4:3: warning: format not a string literal and no format arguments [-Wformat-security]
   printf (argv[1]);
   ^
% ./fmt %s%s%s%s%s%s%s%s
zsh: segmentation fault (core dumped)  ./fmt %s%s%s%s%s%s%s%s
% echo $?
139
% kill -l 11
SEGV
```

- Buffer overflow
```
% cat buf.c
#include <stdio.h>

int main(int argc, char *argv[]) {
  char buf[64];

  sprintf(buf, argv[1]);
  return 0;
}
% ./buf `perl -e 'print "A" x 128'`
*** stack smashing detected ***: ./buf terminated
zsh: abort (core dumped)  ./buf `perl -e 'print "A" x 128'`
% echo $?
134
% kill -l 6  ### 134 - 128 = 6
ABRT
```

- Division by zero
```
% cat divzero.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  printf("Result: %d\n", 1 / atoi(argv[1]));
  return 0;
}

% gcc -o divzero divzero.c
% ./divzero 0
zsh: floating point exception (core dumped)  ./divzero 0
% echo $?
136
% kill -l 8               
FPE
```

So the Linux system I tested this on has stack smashing detection,
format string bugs can trigger segmentation faults, and division by
zero causes a floating point exception. These exit values can all be
caught and analyzed. Any value over 128 in theory should be a
triggered bug unless the programmer took special liberties with their
return values.

Using the subprocess module within Python, I can easily run programs
with fuzz input and catch these errors.
