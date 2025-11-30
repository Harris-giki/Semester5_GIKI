#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Struct to pass arguments to the thread
typedef struct {
    int a;
    int b;
} myarg_t;

// Struct to return results from the thread
typedef struct {
    int sum;
    int product;
} myret_t;

// Thread function
void *mythread(void *arg) {
    myarg_t *args = (myarg_t *)arg;          // cast void* back to original type

    // Allocate memory for return value
    myret_t *retvals = malloc(sizeof(myret_t));
    if (retvals == NULL) {
        perror("malloc failed");
        pthread_exit(NULL);
    }

    // Compute sum and product
    retvals->sum = args->a + args->b;
    retvals->product = args->a * args->b;

    return (void *)retvals;  // return pointer to heap memory
}

int main() {
    pthread_t tid;             // Thread ID
    myarg_t args = {10, 20};   // Arguments to pass to thread
    myret_t *result;           // Pointer to receive return value

    // Create the thread
    if (pthread_create(&tid, NULL, mythread, &args) != 0) {
        perror("pthread_create failed");
        return 1;
    }

    // Wait for thread to finish and get the return value
    if (pthread_join(tid, (void **)&result) != 0) {
        perror("pthread_join failed");
        return 1;
    }

    // Print results
    printf("Sum: %d, Product: %d\n", result->sum, result->product);

    // Free allocated memory
    free(result);

    return 0;
}
