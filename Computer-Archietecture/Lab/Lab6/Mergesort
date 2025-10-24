#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 16
#define SEGMENTS 4

// Simple merge function
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    int L[n1], R[n2];

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2)
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

// Sequential merge sort
void mergesort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergesort(arr, left, mid);
        mergesort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

int main() {
    int arr[N];
    srand(42); // fixed seed for reproducibility

    // Step 1: Generate random array
    printf("Original array:\n");
    for (int i = 0; i < N; i++) {
        arr[i] = rand() % 100;
        printf("%d ", arr[i]);
    }
    printf("\n\n");

    int segment_size = N / SEGMENTS;
    double start = omp_get_wtime();

    // Step 2: Parallel region
    #pragma omp parallel for ordered num_threads(SEGMENTS)
    for (int s = 0; s < SEGMENTS; s++) {
        int left = s * segment_size;
        int right = left + segment_size - 1;

        mergesort(arr, left, right);  // Each thread sorts its part

        // Step 3: Ordered printing
        #pragma omp ordered
        {
            printf("Sorted Segment %d: ", s + 1);
            for (int i = left; i <= right; i++)
                printf("%d ", arr[i]);
            printf("\n");
        }
    }

    double end = omp_get_wtime();
    printf("\nExecution time: %f seconds\n", end - start);

    return 0;
}
