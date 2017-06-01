/* LD_PRELOAD wrapper for getenv() and getopt*()
 *  by Daniel Roberson @dmfroberson
 *
 * This will intercept calls to getopt() functions and getenv() and display
 * environment variable names and the optstrings and long option flags for
 * getopt() functions.
 *
 * usage: $ LD_PRELOAD="./ld_preload-get-vars" /path/to/binary
 *
 * example:
 *  % LD_PRELOAD="./ld_preload-get-vars.so" /bin/mv
 *  getenv(SIMPLE_BACKUP_SUFFIX)
 *  getopt_long(bfint:uvS:TZ)
 *   -> --backup -- has_arg: 2
 *   -> --context -- has_arg: 0
 *   -> --force -- has_arg: 0
 *   -> --interactive -- has_arg: 0
 *   -> --no-clobber -- has_arg: 0
 *   -> --no-target-directory -- has_arg: 0
 *   -> --strip-trailing-slashes -- has_arg: 0
 *   -> --suffix -- has_arg: 1
 *   -> --target-directory -- has_arg: 1
 *   -> --update -- has_arg: 0
 *   -> --verbose -- has_arg: 0
 *   -> --help -- has_arg: 0
 *   -> --version -- has_arg: 0
 *  /bin/mv: missing file operand
 *  Try '/bin/mv --help' for more information.

 */  
#include <stdio.h>
#include <getopt.h>


/* getenv()
 * -- Intercept getenv() and print in ENV:VARNAME="@@" format
 */
char *getenv(const char *name) {
  printf("# %s environment variable\n", name);
  printf("ENV:%s=\"@@\"\n\n", name);

  return NULL;
}


/* getopt()
 * -- Intercept getopt() and print out flags in "-f @@" format if they take
 *    an argument. Otherwise, Leave a comment.
 */
int getopt(int argc, char * const argv[], const char *optstring) {
  int i;


  for (i = 0; optstring[i]; i++) {
    if (optstring[i + 1] == ':') {
      printf("#-%c flag\n", optstring[i]);
      printf("-%c @@\n\n", optstring[i]);
      i++;
    } else {
      printf("# -%c takes no arguments\n", optstring[i]);
    }
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


  for (i = 0; longopts[i].name; i++) {
    if (longopts[i].has_arg) {
      printf("# --%s flag\n", longopts[i].name);
      printf("--%s @@\n\n", longopts[i].name);
    } else {
      printf("# --%s takes no arguments\n", longopts[i].name);
    }
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


  for (i = 0; longopts[i].name; i++) {
    if (longopts[i].has_arg) {
      printf("# --%s flag\n", longopts[i].name);
      printf("--%s @@\n\n", longopts[i].name);
    } else {
      printf("# --%s takes no arguments\n", longopts[i].name);
    }
  }

  return -1;
}
