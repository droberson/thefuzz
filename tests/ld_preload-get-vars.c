/* LD_PRELOAD wrapper for getenv() and getopt*()
 *  by Daniel Roberson @dmfroberson
 *
 * This will intercept calls to getopt() functions and getenv() and display
 * environment variable names and the optstrings and long option flags for
 * getopt() functions.
 *
 * usage: $ LD_PRELOAD="./ld_preload-get-vars.so" /path/to/binary
 *
 * For automated scripting:
 *
 * LD_PRELOAD="./ld_preload-get-vars.so" bin |tac |sed -n '/End\ of\ /,$p' |tac
 *
 * The above example can probably be cleaned up, but you can redirect its
 * output to a file, then use it as a script to fuzz a program against.
 */  
#include <stdio.h>
#include <getopt.h>

/* constructor to print out header
 */
void begin (void) __attribute__((constructor));

void begin(void) {
  printf("###\n");
  printf("### Auto-generated with ld_preload-get-vars.so\n");
  printf("###\n\n");
}


/* getenv()
 * -- Intercept getenv() and print in ENV:VARNAME="@@" format
 */
char *getenv(const char *name) {
  printf("# %s environment variable\n", name);
  printf("ENV:%s=\"@@\"\n", name);
  printf("# End of %s section\n\n", name);

  return NULL;
}


/* getopt()
 * -- Intercept getopt() and print out flags in "-f @@" format if they take
 *    an argument. Otherwise, Leave a comment.
 */
int getopt(int argc, char * const argv[], const char *optstring) {
  int i;


  printf("# getopt() optstring = %s\n", optstring);

  for (i = 0; optstring[i]; i++) {
    if (optstring[i + 1] == ':') {
      printf("# -%c <flag>\n", optstring[i]);
      printf("-%c @@\n\n", optstring[i]);
      i++;
    } else {
      printf("# -%c takes no arguments\n", optstring[i]);
    }

    printf("# End of -%c section\n\n", optstring[i]);
  }

  return -1;
}


/* getopt_long()
 * -- Intercept getopt_long() and print in "--flag @@" format if the flag
 *    accepts an argument. Otherwise, leave a comment.
 */
int getopt_long(int argc, char * const argv[], const char *optstring,
                const struct option *longopts, int *longindex) {
  int i;


  printf("# getopt_long() optstring = %s\n", optstring);

  for (i = 0; optstring[i]; i++) {
    if (optstring[i + 1] == ':') {
      printf("# -%c <flag>\n", optstring[i]);
      printf("-%c @@\n", optstring[i]);
      i++;
    } else {
      printf("# -%c takes no arguments\n", optstring[i]);
    }

    printf("# End of -%c section\n\n", optstring[i]);
  }

  for (i = 0; longopts[i].name; i++) {
    printf("# Start of --%s section\n", longopts[i].name);

    if (longopts[i].has_arg) {
      printf("# --%s <flag>\n", longopts[i].name);
      printf("--%s @@\n\n", longopts[i].name);
    } else {
      printf("# --%s takes no arguments\n", longopts[i].name);
    }

    printf("# End of --%s flag section\n\n", longopts[i].name);
  }

  return -1;
}


/* getopt_long_only()
 * -- Intercept getopt_long_only() and print in "--flag @@" format if the flag
 *    accepts an argument. Otherwise, leave a comment.
 */
int getopt_long_only(int argc, char * const argv[], const char *optstring,
                     const struct option *longopts, int *longindex) {
  int i;


  printf("# getopt_long() optstring = %s\n", optstring);

  for (i = 0; optstring[i]; i++) {
    if (optstring[i + 1] == ':') {
      printf("# -%c <flag>\n", optstring[i]);
      printf("-%c @@\n", optstring[i]);
      i++;
    } else {
      printf("# -%c takes no arguments\n", optstring[i]);
    }
 
    printf("# End of -%c section\n\n", optstring[i]);
  }

  for (i = 0; longopts[i].name; i++) {
    printf("# Start of --%s section\n", longopts[i].name);

    if (longopts[i].has_arg) {
      printf("# --%s <flag>\n", longopts[i].name);
      printf("--%s @@\n", longopts[i].name);
    } else {
      printf("# --%s takes no arguments\n", longopts[i].name);
    }

    printf("# End of --%s flag section\n\n", longopts[i].name);
  }

  return -1;
}
