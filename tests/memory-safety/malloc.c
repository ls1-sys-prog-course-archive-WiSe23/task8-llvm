#include <stdio.h>
#include <stdlib.h>

typedef struct {
  char *username;
  char isAdmin;
} User;

void my_gets(char *buf) {
  char c;
  // Who needs bounds checks anyway?
  while ((c = getc(stdin)) != '\n') {
    *buf++ = c;
  }
  *buf = '\0';
}

int main() {
  User *user = malloc(sizeof(User));
  // no username is longer than 31 bytes + nullpointer, right?
  user->username = malloc(32);

  printf("Enter your name: ");
  my_gets(user->username);

  if (user->isAdmin) {
    printf("Hello admin %s\n", user->username);
  } else {
    printf("Hello normal user %s\n", user->username);
  }

  free(user->username);
  free(user);

  return 0;
}
