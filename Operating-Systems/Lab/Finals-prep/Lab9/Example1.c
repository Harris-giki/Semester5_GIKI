#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

void *myThreadFunct(void *varg)
{
    sleep(1);
    printf("this simulated the thread function\n");
    return NULL;
}

int main()
{
    pthread_t thread_id;
    printf("Before thread\n");
    pthread_create(&thread_id, NULL, myThreadFunct,NULL);
    pthread_join(&thread_id, NULL);
    printf("After Thread\n");
    exit(0);
}