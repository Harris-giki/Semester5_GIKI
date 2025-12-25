#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

int sz = 100;
int num_threads = 4;

typedef struct {
    int st_ind;
    int en_ind;
    int* A;
    int iter;
} arguments;

void* thread_worker(void* args1) {
    arguments* args = args1;
    int sum = 0;

    for (int i = args->st_ind; i < args->en_ind; i++)
        sum += args->A[i];

    printf("The sum from thread %d is %d\n", args->iter, sum);

    int* val = malloc(sizeof(int));
    *val = sum;
    return val;
}

int main() {
    pthread_t t_id[num_threads];
    int* Arr = calloc(sz, sizeof(int));

    for (int i = 0; i < sz; i++)
        Arr[i] = i + 1;

    arguments args[num_threads];

    for (int i = 0; i < num_threads; i++) {
        args[i].st_ind = (i * sz) / num_threads;
        args[i].en_ind = ((i + 1) * sz) / num_threads;
        args[i].A = Arr;
        args[i].iter = i;

        if (pthread_create(&t_id[i], NULL, thread_worker, &args[i]) != 0) {
            perror("pthread_create failed");
            exit(1);
        }
    }

    int global_sum = 0;
    for (int i = 0; i < num_threads; i++) {
        int* temp_sum;
        pthread_join(t_id[i], (void**)&temp_sum);
        global_sum += *temp_sum;
        free(temp_sum);
    }

    printf("The global sum is %d\n", global_sum);

    free(Arr);
    return 0;
}
