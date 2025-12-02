#include <stdio.h>
#include <pthread.h>

volatile int done = 0; // volatile tells the compiler to re-check for the value of this variable again and again
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER; // initialized mutex (a lock) to protect shared data
pthread_cond_t c = PTHREAD_COND_INITIALIZER; // condition variable by which threads can sleep and be woken up


// the helper function that child calls when it is finished
void thr_exit()
{
    pthread_mutex_lock(&m);
    done = 1;
    pthread_cond_signal(&c);
    pthread_mutex_unlock(&m);
}

// the child thread function
void *child (void *arg)
{
    printf("Child\n");
    thr_exit();
    return NULL;
}

// helper function that parent calls to wait for the child
void thr_join()
{
    pthread_mutex_lock(&m);
    while(done == 0)
    {
        pthread_cond_wait(&c, &m); // atomically unlocks m and puts the thread to sleep waiting for c
        // When woken, cond_wait will automatically re-lock m before returning
    }
    // lock then released below:
    pthread_mutex_unlock(&m);
    // used mutex here to perform the check and sleeping of the parent thread atomically so that no interrupts in btw occur
    // thus there is no case of the value of done being changed after it was checked by the parent (which would be thus missed)
    // an important use case of mutex
}

int main(int argc, char *argv[]) {
    printf("parent: begin\n");
    pthread_t p;
    pthread_create(&p, NULL, child, NULL);
    thr_join();
    printf("parent: end\n");
    return 0;
}

// prints "parent: begin".

// creates the child thread (which will run child()).

// calls thr_join() — waits (sleeping) until done becomes 1.

// after child finished and parent was woken, parent prints "parent: end".

// exit program.

// say the signal by child was scheduled earlier and is now lost before the parent runs
// if the parent doesn't catches this signal it could go into sleep forever, to prevent this we use state variables like done
// that changes value as per the issuance of th signal, thus the signal is lost but the variable is never lost
