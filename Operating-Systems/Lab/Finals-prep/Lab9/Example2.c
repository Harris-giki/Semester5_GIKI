#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int g =0;
void *mythreadfunct(void *arg)
{
    int *myid = (int *) arg;
    static int s = 0;
    ++s, ++g;
    printf("Thread ID: %d, Static: %d, Global: %d\n,", *myid, s,g);
}
void *mythreadfunct1(void *arg)
{
    int *myid = (int *) arg;
    static int s = 0;
    ++s, ++g;
    printf("Thread ID: %d, Static: %d, Global: %d\n,", *myid, s,g);
}

int main()
{
    int i;
    pthread_t tid;
    for(i=0; i<3; i++)
    {
        pthread_create(&tid, NULL, mythreadfunct, (void *)&tid );
    }
    for(i=0; i<3; i++)
    {
        pthread_create(&tid, NULL, mythreadfunct1, (void *)&tid );
    }

    pthread_exit(NULL);
 return 0;
}
// but race conditions can occur