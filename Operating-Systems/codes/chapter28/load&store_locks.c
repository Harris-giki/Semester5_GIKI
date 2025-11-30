#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

// load and store implementation of locks
// this implementation is not safe for real systems


typedef struct __lock_t
{
    int flag;
}lock_t

void init(lock_t *giveLock)
{
    givenLock->flag=0;
}

voic lock (lock_t *givenLock)
{
    while(givenLock->flag==1)
    {
        //spin the lock i.e the lock is in hold of a thread
    };
    givenLock->flag = 1; //acquire the lock
}
// Release lock
void unlock(lock_t *givenLock) {
    givenLock->flag = 0;
}

void *worker_task (void *arg) // any return type with any type of arguments
{
    lock_t *sharedLock  = (lock_t *)arg; // type casting
    rintf("Thread %lu: attempting to enter critical section...\n",
           pthread_self());

    lock(sharedLock);

    // --- critical section ---
    printf("Thread %lu: inside critical section\n", pthread_self());
    usleep(50000);  // simulate some work
    // ------------------------

    unlock(sharedLock);

    printf("Thread %lu: exited critical section\n", pthread_self());

    return NULL;
}

int main()
{
    p_thread firstThread, secondThread;

    lock_t coordinatorLock;

    init(&coordinatorLock);

    pthread_create(&firstThread, NULL, worker_task, &coordinatorLock)
    pthread_create(&secondThread, NULL, worker_task, &coordinatorLock)
    
    pthread_join(firstThread,NULL);
    pthread_join(secondThread,NULL);
}