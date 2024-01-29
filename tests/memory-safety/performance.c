#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((noinline)) void init_ptrs(void **ptrs, size_t allocations,
                                         size_t size) {
  for (int i = 0; i < allocations; ++i) {
    ptrs[i] = malloc(size);
    if (!ptrs[i]) {
      fprintf(stderr, "malloc failed\n");
      exit(1);
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "usage: %s [allocations] [size] [invalid_access?]\n",
            argv[0]);
    return 1;
  }
  char invalid_access = argc == 4 ? 1 : 0;

  size_t allocations = atoll(argv[1]);
  size_t size = atoll(argv[2]);

  char **ptrs = malloc(allocations * sizeof(char *));
  if (!ptrs) {
    fprintf(stderr, "malloc failed\n");
    return 1;
  }

  // if invalid_access is set, we will do out-of-bounds access in this function.
  init_ptrs((void **)ptrs, allocations + invalid_access, size);

  printf("Allocated %zu blocks of size %zu, in total %f GiB\n", allocations,
         size, allocations * size / (1024.0 * 1024.0 * 1024.0));

  for (int i = 0; i < allocations; ++i) {
    // make sure to touch every 100th byte to stress performance
    for (int j = 0; j < size; j += 100) {
      ptrs[i][j] = ptrs[i][j] + 1;
    }
  }

  for (int i = 0; i < allocations; ++i) {
    free(ptrs[i]);
  }

  free(ptrs);
}
