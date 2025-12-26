// What your code is trying to do

// Create an array of 100 integers 1, 2, ..., 100.

// Create a shared variable sum to hold the final result.

// Use parallel region to split the work among threads.

// Each thread computes a local sum of its assigned chunk of the array.

// Use #pragma omp atomic to safely add the thread's local sum to the shared sum.

#include <stdio.h>
#include <omp.h>

int main() {
    int arr[100];
    int sum = 0;

    // Initialize array
    for (int i = 0; i < 100; i++)
        arr[i] = i + 1;

    #pragma omp parallel
    {
        int local_sum = 0;

        #pragma omp for
        for(int i = 0; i < 100; i++) {
            local_sum += arr[i];
        }

        // Safely add local sum to shared sum
        #pragma omp atomic
        sum += local_sum;
    }

    printf("Sum = %d\n", sum);
    return 0;
}
