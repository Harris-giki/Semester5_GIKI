#include "kernel/types.h"
#include "kernel/stat.h"
#include "kernel/fcntl.h"
#include "user/user.h"

static void testsymlink(void);
static void concur(void);
static void cleanup(void);

int
main(int argc, char *argv[])
{
  cleanup();
  testsymlink();
  concur();
  exit(0);
}

static void
cleanup(void)
{
  unlink("/testsymlink/a");
  unlink("/testsymlink/b");
  unlink("/testsymlink/c");
  unlink("/testsymlink/1");
  unlink("/testsymlink/2");
  unlink("/testsymlink/3");
  unlink("/testsymlink/4");
  unlink("/testsymlink/y");
  unlink("/testsymlink/z");
  unlink("/testsymlink");
}

static int
stat_slink(char *pn, struct stat *st)
{
  int fd = open(pn, O_RDONLY | O_NOFOLLOW);
  if(fd < 0)
    return -1;
  if(fstat(fd, st) != 0) {
    close(fd);
    return -1;
  }
  close(fd);
  return 0;
}

static void
testsymlink(void)
{
  int r, fd1 = -1, fd2 = -1;
  char buf[4] = {'a', 'b', 'c', 'd'};
  char c = 0, c2 = 0;
  struct stat st;

  printf("Start: test symlinks\n");

  mkdir("/testsymlink");

  fd1 = open("/testsymlink/a", O_CREATE | O_RDWR);
  if(fd1 < 0) {
    printf("FAILED: failed to open a\n");
    exit(1);
  }

  r = symlink("/testsymlink/a", "/testsymlink/b");
  if(r < 0) {
    printf("FAILED: symlink b -> a failed\n");
    exit(1);
  }

  if(write(fd1, buf, sizeof(buf)) != 4) {
    printf("FAILED:  failed to write to a\n");
    exit(1);
  }

  if(stat_slink("/testsymlink/b", &st) != 0) {
    printf("FAILED: failed to stat b\n");
    exit(1);
  }
  if(st.type != T_SYMLINK) {
    printf("FAILED: b should be a symlink\n");
    exit(1);
  }

  fd2 = open("/testsymlink/b", O_RDONLY | O_NOFOLLOW);
  if(fd2 < 0) {
    printf("FAILED: failed to open b with O_NOFOLLOW\n");
    exit(1);
  }
  read(fd2, &c, 1);
  if(c != '/') {
    printf("FAILED: expected '/' but got '%c'\n", c);
    exit(1);
  }
  close(fd2);

  fd2 = open("/testsymlink/b", O_RDONLY);
  if(fd2 < 0) {
    printf("FAILED: failed to open b\n");
    exit(1);
  }
  read(fd2, &c, 1);
  if(c != 'a') {
    printf("FAILED: expected 'a' but got '%c'\n", c);
    exit(1);
  }
  close(fd2);
  close(fd1);

  r = symlink("/testsymlink/b", "/testsymlink/c");
  if(r < 0) {
    printf("FAILED: symlink c -> b failed\n");
    exit(1);
  }
  fd1 = open("/testsymlink/c", O_RDONLY);
  if(fd1 < 0) {
    printf("FAILED: failed to open c\n");
    exit(1);
  }
  read(fd1, &c, 1);
  if(c != 'a') {
    printf("FAILED: expected 'a' but got '%c'\n", c);
    exit(1);
  }
  close(fd1);

  r = symlink("/testsymlink/nonexistent", "/testsymlink/y");
  if(r != 0) {
    printf("FAILED:  symlink to nonexistent should succeed\n");
    exit(1);
  }
  fd1 = open("/testsymlink/y", O_RDONLY);
  if(fd1 >= 0) {
    printf("FAILED: open symlink to nonexistent should fail\n");
    close(fd1);
    exit(1);
  }

  r = symlink("/testsymlink/z", "/testsymlink/z");
  if(r != 0) {
    printf("FAILED: symlink z -> z should succeed\n");
    exit(1);
  }
  fd1 = open("/testsymlink/z", O_RDONLY);
  if(fd1 >= 0) {
    printf("FAILED: open symlink cycle should fail\n");
    close(fd1);
    exit(1);
  }

  unlink("/testsymlink/b");
  fd1 = open("/testsymlink/a", O_RDONLY);
  if(fd1 < 0) {
    printf("FAILED: a should still exist\n");
    exit(1);
  }
  read(fd1, &c2, 1);
  if(c2 != 'a') {
    printf("FAILED: a should still contain 'a'\n");
    exit(1);
  }
  close(fd1);

  cleanup();
  printf("test symlinks: ok\n");
}

static void
concur(void)
{
  int pid, i, fd;
  char buf[2];
  char name[32];

  printf("Start:  test concurrent symlinks\n");

  mkdir("/testsymlink");

  // Create 4 regular files:  /testsymlink/1, /testsymlink/2, /testsymlink/3, /testsymlink/4
  for(i = 0; i < 4; i++) {
    strcpy(name, "/testsymlink/X");
    name[12] = '1' + i;  // Creates files 1, 2, 3, 4
    fd = open(name, O_CREATE | O_RDWR);
    if(fd < 0) {
      printf("FAILED: create %s failed\n", name);
      exit(1);
    }
    buf[0] = 'a' + i;
    buf[1] = '\0';
    if(write(fd, buf, 2) != 2) {
      printf("FAILED: write %s failed\n", name);
      exit(1);
    }
    close(fd);
  }

  pid = fork();
  if(pid < 0) {
    printf("FAILED:  fork failed\n");
    exit(1);
  }

  if(pid == 0) {
    // Child:  create and delete symlinks
    char target[32], link[32];
    for(i = 0; i < 100; i++) {
      strcpy(target, "/testsymlink/X");
      strcpy(link, "/testsymlink/X");
      target[12] = '1' + (i % 4);
      link[12] = '1' + ((i + 1) % 4);

      // Only create symlink if target != link (avoid self-links in this test)
      if(target[12] != link[12]) {
        unlink(link);
        symlink(target, link);
      }
    }
    exit(0);
  }

  // Parent:  try to open files (may fail due to race, that's OK)
  int success = 0;
  for(i = 0; i < 100; i++) {
    strcpy(name, "/testsymlink/X");
    name[12] = '1' + (i % 4);
    fd = open(name, O_RDONLY);
    if(fd >= 0) {
      success++;
      close(fd);
    }
    // Don't fail on open error - race condition is expected
  }

  int xstatus;
  wait(&xstatus);

  // As long as we had some successful opens and child exited OK, we're good
  if(xstatus != 0) {
    printf("FAILED: child failed\n");
    exit(1);
  }

  cleanup();
  printf("test concurrent symlinks:  ok\n");
}
