#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define NUM_THREADS 3

pthread_barrier_t barrier;

void* worker(void* arg) {
    int id = *(int*)arg;

    printf("Thread %d: before barrier\n", id);

    // Wait at the barrier
    pthread_barrier_wait(&barrier);

    printf("Thread %d: after barrier\n", id);

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    // Initialize barrier for NUM_THREADS threads
    pthread_barrier_init(&barrier, NULL, NUM_THREADS);

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i;
        pthread_create(&threads[i], NULL, worker, &ids[i]);
    }

    // Wait for threads to finish
    for (int i = 0; i < NUM_THREADS; i++)
        pthread_join(threads[i], NULL);

    // Destroy barrier
    pthread_barrier_destroy(&barrier);

    return 0;
}
