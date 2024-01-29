#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  volatile int *values = malloc(4 * sizeof(int));

  values[0] = argc;

  printf("Before: %d\n", values[0]);

  if (argc > 1) {
    free((void *)values);
  }

  printf("After: %d\n", values[0]);
  free((void *)values);

  return 0;
}
