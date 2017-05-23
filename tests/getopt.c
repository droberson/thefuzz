#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>


void usage(char *progname) {
  printf("usage: %s [-b <buf>] [-f <fmt>] [-d <div>] [-h] <str>\n", progname);
  exit(EXIT_FAILURE);
}

int main(int argc, char *argv[]) {
  int opt;
  int dividend;
  char buf[512];
  char *heap;


  if (argc == 1)
    usage(argv[0]);

  printf("This is a buggy program!\n");

  while ((opt = getopt(argc, argv, "b:f:d:h")) != -1) {
    switch (opt) {
    case 'b':
      sprintf(buf, "%s", optarg);
      break;

    case 'f':
      printf(optarg);
      break;

    case 'd':
      printf("1 / %d = %d\n", atoi(optarg), 1 / atoi(optarg));
      break;

    default:
    case 'h':
      usage(argv[0]);
    }
  }

  argc -= optind;
  argv += optind;

  if (argc > 0) {
    heap = (char *)malloc(32);
    strcpy(heap, argv[0]);

    printf("You entered: %s\n", heap);

    free(heap);
  }

  return EXIT_SUCCESS;
}

