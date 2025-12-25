#include <stdio.h> 
#include <pthread.h> 
#include <stdlib.h>

#define VALUE_COUNT_MAX 5
int value[VALUE_COUNT_MAX];       // Shared buffer
int value_count = 0;              // Number of items currently in the buffer
pthread_mutex_t value_mtx;        // Mutex to protect shared data
pthread_cond_t value_cnd;         // Condition variable to signal availability

void *run(void *arg)
{
    (void)arg;

    for (;;) {
        pthread_mutex_lock(&value_mtx);  // Lock before accessing shared data

        while (value_count < VALUE_COUNT_MAX) {
            printf("Thread: is waiting\n");
            pthread_cond_wait(&value_cnd, &value_mtx); // Wait until buffer is full
        }

        printf("Thread: is awake!\n");
        int t = 0;

        // Sum all values
        for (int i = 0; i < VALUE_COUNT_MAX; i++)
            t += value[i];

        printf("Thread: total is %d\n", t);

        // Reset buffer
        value_count = 0;

        pthread_mutex_unlock(&value_mtx);  // Unlock mutex for main thread
    }
    return 0;
}
int main(void)
{
    pthread_t t;

    // Spawn worker thread
    pthread_create(&t, NULL, run, NULL);
    pthread_detach(t); // Thread will clean up automatically

    // Initialize synchronization primitives
    pthread_mutex_init(&value_mtx, NULL);
    pthread_cond_init(&value_cnd, NULL);

    for (;;) {
        int n;
        scanf("%d", &n);

        pthread_mutex_lock(&value_mtx);
        value[value_count++] = n;  // Add value to buffer

        if (value_count == VALUE_COUNT_MAX) {
            printf("Main: signaling thread\n");
            pthread_cond_signal(&value_cnd);  // Signal worker thread
        }

        pthread_mutex_unlock(&value_mtx);
    }

    pthread_mutex_destroy(&value_mtx);
    pthread_cond_destroy(&value_cnd);
}
