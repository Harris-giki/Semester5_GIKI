#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int data = 0;                  // Shared data
int ready = 0;                 // Flag to indicate data availability
pthread_mutex_t mtx;
pthread_cond_t cond;

void* producer(void* arg) {
    (void)arg;
    // Produce a value
    pthread_mutex_lock(&mtx);
    data = 42;
    ready = 1;
    printf("Producer: produced data = %d\n", data);
    pthread_cond_signal(&cond); // Signal consumer
    pthread_mutex_unlock(&mtx);
    return NULL;
}

void* consumer(void* arg) {
    (void)arg;
    pthread_mutex_lock(&mtx);
    // Wait until data is ready
    while (!ready) {
        pthread_cond_wait(&cond, &mtx);
    }
    printf("Consumer: consumed data = %d\n", data);
    pthread_mutex_unlock(&mtx);
    return NULL;
}

int main() {
    pthread_t t1, t2;

    pthread_mutex_init(&mtx, NULL);
    pthread_cond_init(&cond, NULL);

    pthread_create(&t1, NULL, consumer, NULL);
    pthread_create(&t2, NULL, producer, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    pthread_mutex_destroy(&mtx);
    pthread_cond_destroy(&cond);

    return 0;
}
