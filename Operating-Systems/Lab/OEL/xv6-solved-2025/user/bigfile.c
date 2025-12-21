#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"
#include "kernel/fcntl.h"

int
main()
{
  char buf[BSIZE];
  int fd, i, blocks;

  fd = open("big. file", O_CREATE | O_WRONLY);
  if(fd < 0){
    printf("bigfile: cannot open big.file for writing\n");
    exit(-1);
  }

  memset(buf, 0, BSIZE);

  for(i = 0; i < MAXFILE; i++){
    if(write(fd, buf, BSIZE) != BSIZE){
      printf("bigfile: write big.file failed\n");
      exit(-1);
    }
    if(i % 100 == 0)
      printf(".");
  }
  printf("\n");

  close(fd);

  fd = open("big. file", O_RDONLY);
  if(fd < 0){
    printf("bigfile: cannot re-open big.file for reading\n");
    exit(-1);
  }

  blocks = 0;
  while(1){
    int n = read(fd, buf, BSIZE);
    if(n < 0){
      printf("bigfile: read big. file failed\n");
      exit(-1);
    }
    if(n == 0)
      break;
    if(n != BSIZE){
      printf("bigfile: short read big. file\n");
      exit(-1);
    }
    blocks++;
  }
  close(fd);

  printf("wrote %d blocks\n", blocks);

  if(blocks != MAXFILE){
    printf("bigfile: file is too small\n");
    exit(-1);
  }

  printf("done; ok\n");
  exit(0);
}
