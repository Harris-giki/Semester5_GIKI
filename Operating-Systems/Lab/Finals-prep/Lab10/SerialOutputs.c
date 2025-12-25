#include <stdio.h>
#include <pthread.h>

pthread_mutex_t serial_mtx; // mutex

void* run(void* arg) {
    (void)arg;
    static int serial = 0;

    pthread_mutex_lock(&serial_mtx);
    printf("Thread running! %d\n", serial);
    serial++;
    pthread_mutex_unlock(&serial_mtx);

    return NULL;
}

#define THREAD_COUNT 10

int main(void) {
    pthread_t t[THREAD_COUNT];

    // Initialize mutex
    pthread_mutex_init(&serial_mtx, NULL);

    // Create threads
    for (int i = 0; i < THREAD_COUNT; i++) {
        pthread_create(&t[i], NULL, run, NULL);
    }

    // Join threads
    for (int i = 0; i < THREAD_COUNT; i++) {
        pthread_join(t[i], NULL);
    }

    // Destroy mutex
    pthread_mutex_destroy(&serial_mtx);

    return 0;
}
