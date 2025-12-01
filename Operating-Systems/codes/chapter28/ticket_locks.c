#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

// ----------------------------
// Fetch-and-Add atomic style (NOT truly atomic in pure C, but for demo)
// ----------------------------
int FetchAndAdd(int *ptr) {
    int old = *ptr;
    *ptr = old + 1;
    return old;
}

// ----------------------------
// Ticket Lock Structure
// ----------------------------
typedef struct __lock_t {
    int ticket;     // next ticket to give
    int turn;       // ticket being served
} lock_t;

// ----------------------------
// Initialize the lock
// ----------------------------
void lock_init(lock_t *lock) {
    lock->ticket = 0;
    lock->turn = 0;
}

// ----------------------------
// Lock: take a ticket and wait your turn
// ----------------------------
void lock(lock_t *lock) {
    int myturn = FetchAndAdd(&lock->ticket); // get my ticket
    while (lock->turn != myturn)
        ; // spin until your ticket is served
}

// ----------------------------
// Unlock: serve next ticket
// ----------------------------
void unlock(lock_t *lock) {
    lock->turn = lock->turn + 1;
}

// ----------------------------
// Worker Thread Function
// ----------------------------
void *worker(void *arg) {
    lock_t *L = (lock_t *)arg;

    printf("Thread %lu: waiting for lock...\n", pthread_self());
    lock(L);

    // --- Critical Section ---
    printf("Thread %lu: inside critical section\n", pthread_self());
    usleep(50000); // simulate work
    // ------------------------

    unlock(L);
    printf("Thread %lu: leaving critical section\n", pthread_self());

    return NULL;
}

int main() {
    pthread_t t1, t2, t3;
    lock_t myLock;

    lock_init(&myLock);

    pthread_create(&t1, NULL, worker, &myLock);
    pthread_create(&t2, NULL, worker, &myLock);
    pthread_create(&t3, NULL, worker, &myLock);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    return 0;
}
