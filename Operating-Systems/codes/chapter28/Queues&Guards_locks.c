#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>


int TestAndSet(int *old_ptr, int new) {
    int old = *old_ptr; // fetch old value at old_ptr
    *old_ptr = new; // store ’new’ into old_ptr
    return old; // return the old value
}


// *   Simple Queue       *
typedef struct node {
    long tid;
    struct node *next;
} node_t;

typedef struct queue {
    node_t *head;
    node_t *tail;
} queue_t;

void queue_init(queue_t *q) {
    q->head = q->tail = NULL;
}

void queue_add(queue_t *q, long tid) {
    node_t *n = malloc(sizeof(node_t));
    n->tid = tid;
    n->next = NULL;

    if (q->tail == NULL) {
        q->head = q->tail = n;
    } else {
        q->tail->next = n;
        q->tail = n;
    }
}

int queue_empty(queue_t *q) {
    return q->head == NULL;
}

long queue_remove(queue_t *q) {
    if (queue_empty(q)) return -1;

    node_t *n = q->head;
    long tid = n->tid;
    q->head = n->next;

    if (q->head == NULL)
        q->tail = NULL;

    free(n);
    return tid;
}

/***********************
 * park/unpark (FAKE)  *
 ***********************/
pthread_mutex_t park_lock = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t park_cv = PTHREAD_COND_INITIALIZER;

// map tid → parked status
pthread_mutex_t sleep_map_lock = PTHREAD_MUTEX_INITIALIZER;
int should_wake[128] = {0};

void park() {
    long tid = pthread_self() % 128;

    pthread_mutex_lock(&sleep_map_lock);
    while (!should_wake[tid]) {
        pthread_cond_wait(&park_cv, &sleep_map_lock);
    }
    should_wake[tid] = 0;
    pthread_mutex_unlock(&sleep_map_lock);
}

void unpark(long tid) {
    tid = tid % 128;

    pthread_mutex_lock(&sleep_map_lock);
    should_wake[tid] = 1;
    pthread_cond_broadcast(&park_cv);
    pthread_mutex_unlock(&sleep_map_lock);
}

/***********************
 *   Lock Structure    *
 ***********************/
typedef struct __lock_t {
    int flag;
    int guard;
    queue_t q;
} lock_t;

void lock_init(lock_t *m) {
    m->flag = 0;
    m->guard = 0;
    queue_init(&m->q);
}

void lock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ; // spin for guard

    if (m->flag == 0) {
        m->flag = 1;       // acquired
        m->guard = 0;
    } else {
        long tid = pthread_self();
        queue_add(&m->q, tid);
        m->guard = 0;
        park();            // sleep
    }
}

void unlock(lock_t *m) {
    while (TestAndSet(&m->guard, 1) == 1)
        ; // spin for guard

    if (queue_empty(&m->q)) {
        m->flag = 0;
    } else {
        long next = queue_remove(&m->q);
        unpark(next);
    }

    m->guard = 0;
}

/***********************
 *  Worker Thread      *
 ***********************/
lock_t mylock;

void *worker(void *arg) {
    int id = (int)(long)arg;

    printf("Thread %d trying to lock...\n", id);
    lock(&mylock);

    printf("Thread %d acquired lock!\n", id);
    usleep(100000);  // simulate critical section

    printf("Thread %d unlocking...\n", id);
    unlock(&mylock);

    return NULL;
}

/***********************
 *       Main          *
 ***********************/
int main() {
    pthread_t t[5];
    lock_init(&mylock);

    for (int i = 0; i < 5; i++)
        pthread_create(&t[i], NULL, worker, (void *)(long)i);

    for (int i = 0; i < 5; i++)
        pthread_join(t[i], NULL);

    return 0;
}
