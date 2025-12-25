#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int max;
int counter = 0;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *mythread(void *arg)
{
    char *letter = (char *)arg;

    for (int i = 0; i < max; i++) {
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }

    printf("Thread %s completed\n", letter);
    return NULL;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: %s <loopcount>\n", argv[0]);
        exit(1);
    }

    max = atoi(argv[1]);

    pthread_t p1, p2;

    printf("Thread process begins\n");

    pthread_create(&p1, NULL, mythread, "A");
    pthread_create(&p2, NULL, mythread, "B");

    pthread_join(p1, NULL);
    pthread_join(p2, NULL);

    printf("Done\n");
    printf("Final counter value: %d\n", counter);

    return 0;
}
