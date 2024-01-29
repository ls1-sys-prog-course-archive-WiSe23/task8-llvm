#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) int read_memory_at(int *memory, int index) {
  return memory[index];
}

int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "usage: %s [index]\n", argv[0]);
    return 1;
  }
  int index = atoi(argv[1]);
  int arr[32];
  for (int i = 0; i < 32; ++i) {
    arr[i] = i;
  }

  printf("arr[%d] = 0x%x\n", index, read_memory_at(arr, index));
  return 0;
}
