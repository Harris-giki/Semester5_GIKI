#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

    int TestAndSet(int *old_ptr, int new) {
    int old = *old_ptr; // fetch old value at old_ptr
    *old_ptr = new; // store ’new’ into old_ptr
    return old; // return the old value
}
typedef struct __lock_t {
    int flag;   // 0 = free, 1 = locked
} lock_t;

void init(lock_t *lock) {
    lock->flag = 0;   // lock initially free
}

void lock(lock_t *lock) {
    // Spin while lock is unavailable
    while (TestAndSet(&lock->flag, 1) == 1) {
        ; // do nothing
    }
}

void unlock(lock_t *lock) {
    lock->flag = 0;
}

void *worker_task(void *arg) {
    lock_t *sharedLock = (lock_t *)arg;

    printf("Thread %lu: attempting to acquire lock...\n", pthread_self());

    lock(sharedLock);

    // -------- CRITICAL SECTION --------
    printf("Thread %lu: inside critical section\n", pthread_self());
    usleep(50000);  // simulate some work
    // ----------------------------------

    unlock(sharedLock);

    printf("Thread %lu: exited critical section\n", pthread_self());
    return NULL;
}

int main() {
    pthread_t t1, t2;
    lock_t myLock;

    init(&myLock);

    pthread_create(&t1, NULL, worker_task, &myLock);
    pthread_create(&t2, NULL, worker_task, &myLock);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}
