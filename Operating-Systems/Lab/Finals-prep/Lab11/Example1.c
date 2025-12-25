#define _XOPEN_SOURCE 600
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define NUM_THREADS 6
#define NUM_ITERATIONS 10

pthread_barrier_t barrier;

void* thread_function(void* arg) {
    int my_number = *(int*)arg;

    for (int i = 0; i < NUM_ITERATIONS; i++) {
        printf("Thread %d, iteration %d\n", my_number, i);

        // Wait at the barrier for all threads
        int result = pthread_barrier_wait(&barrier);
        if (result != 0 && result != PTHREAD_BARRIER_SERIAL_THREAD) {
            perror("Could not wait on barrier");
            exit(EXIT_FAILURE);
        }
    }

    printf("Bye from thread %d\n", my_number);
    pthread_exit(NULL);
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_id[NUM_THREADS];

    // Initialize the barrier
    if (pthread_barrier_init(&barrier, NULL, NUM_THREADS) != 0) {
        perror("Could not create a barrier");
        exit(EXIT_FAILURE);
    }

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_id[i] = i;
        if (pthread_create(&threads[i], NULL, thread_function, &thread_id[i]) != 0) {
            perror("Thread creation failed");
            exit(EXIT_FAILURE);
        }
    }

    printf("Waiting for threads to finish...\n");

    // Join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            perror("pthread_join failed");
        } else {
            printf("Picked up a thread\n");
        }
    }

    // Destroy barrier
    pthread_barrier_destroy(&barrier);

    printf("All done\n");
    return 0;
}
