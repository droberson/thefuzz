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


char *getenv(const char *name) {
  printf("getenv(%s)\n", name);

  return NULL;
}

int getopt(int argc, char * const argv[], const char *optstring) {
  printf("getopt(%s)\n", optstring);

  return -1;
}
 
int getopt_long(int argc, char * const argv[], const char *optstring,
                const struct option *longopts, int *longindex) {
  int i;


  printf("getopt_long(%s)\n", optstring);

  for (i = 0; longopts[i].name; i++)
    printf(" -> --%s -- has_arg: %d\n", longopts[i].name, longopts[i].has_arg);

  return -1;
}

int getopt_long_only(int argc, char * const argv[], const char *optstring,
                     const struct option *longopts, int *longindex) {
  int i;


  printf("getopt_long_only(%s)\n", optstring);

  for (i = 0; longopts[i].name; i++)
    printf(" -> --%s -- has_arg: %d\n", longopts[i].name, longopts[i].has_arg);

  return -1;
}

