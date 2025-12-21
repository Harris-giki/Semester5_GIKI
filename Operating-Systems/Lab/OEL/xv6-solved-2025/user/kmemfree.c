#include "kernel/types.h"
#include "user/user.h"
#include "kernel/stat.h"

int main(){
  printf("hello welcome to xv6");
  int free = kmemfree();
  printf("\n freed = %d Mb", free/1048576);
  return 0;
}
