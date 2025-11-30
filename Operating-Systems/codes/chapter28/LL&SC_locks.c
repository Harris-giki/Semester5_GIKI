#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

typedef struct __lock_t
{
    int flag;
}lock_t

void init(lock_t *giveLock)
{
    givenLock->flag=0;
}

int LoadLinked(int *ptr)
{
    return *ptr;
}

int storeConditional(int *ptr, int value)
{
    // if(no update to *ptr since LL to this address)
     /*
        In real hardware, SC only succeeds if *targetAddr
        hasn't been modified since the LL.

        We cannot simulate that properly in simple C,
        so we pretend success for now.
    */
    *ptr = value;
    return 1;

    else
    {
        return 0;
    }
}

void lock(lock_t *lock)
{
    while(1)
    {
        // Step 1: Wait until lock turns 0
        while(LoadLinked(&lock->flag)==1)
        {
        ; //spin until it's zero
        }
        
        // Step 2: Try to set lock to 1
        if(storeConditional(&lock->flag,1)==1)
            return; // Got the lock!
                    
    }
    //otherwise: try again
}

void unlock(lock_t *lock)
{
    lock->flag=0
}