#include "kernel/types.h"
#include "user/user.h"
#include "kernel/stat.h"


int main(int argc ,char **argv){

int ticks=atoi(argv[1]);
if(ticks<=0) {
  printf("failed");
  return 0;

}
pause(ticks);


  return 0;
}
