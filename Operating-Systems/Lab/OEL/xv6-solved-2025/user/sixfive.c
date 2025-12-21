#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fcntl.h"

#define SEP " -\r\t\n./,"

int is_sep(char c) {
  char *p = SEP;
  while (*p) {
    if (*p == c)
      return 1;
    p++;
  }
  return 0;
}

int is_digit(char c) {
  return c >= '0' && c <= '9';
}

int
main(int argc, char *argv[])
{
  if (argc < 2) {
    fprintf(2, "Usage: sixfive file...\n");
    exit(1);
  }

  char buf[512];

  for (int f = 1; f < argc; f++) {
    int fd = open(argv[f], O_RDONLY);
    if (fd < 0) {
      fprintf(2, "sixfive: cannot open %s\n", argv[f]);
      continue;
    }

    int num = 0;
    int in_num = 0;

    int n;
    while ((n = read(fd, buf, sizeof(buf))) > 0) {
      for (int i = 0; i < n; i++) {
        char c = buf[i];

        if (is_digit(c)) {
          num = num * 10 + (c - '0');
          in_num = 1;
        } else {
          if (in_num) {
            // end of a number
            if (num % 5 == 0 || num % 6 == 0) {
              // print number
              printf("%d\n", num);
            }
            // reset
            num = 0;
            in_num = 0;
          }
          // ignore this separator
        }
      }
    }

    // handle number ending at EOF
    if (in_num) {
      if (num % 5 == 0 || num % 6 == 0) {
        printf("%d\n", num);
      }
    }

    close(fd);
  }

  exit(0);
}
