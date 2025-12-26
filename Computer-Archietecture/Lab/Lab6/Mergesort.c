#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 16        // Array size
#define SEGMENTS 4  // Number of parallel segments

// Merge function
void merge(int arr[], int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    int *L = (int*)malloc(n1 * sizeof(int));
    int *R = (int*)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2)
        arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];

    free(L);
    free(R);
}

// Standard sequential merge sort
void mergesort(int arr[], int left, int right) {
    if (left < right) {
        int mid = left + (right - left)/2;
        mergesort(arr, left, mid);
        mergesort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}

// Merge two segments: left1-right1 with left2-right2
void merge_segments(int arr[], int left1, int right1, int left2, int right2) {
    merge(arr, left1, right1, right2);
}

int main() {
    int arr[N];
    srand(42);

    // Generate random array
    printf("Original array:\n");
    for (int i = 0; i < N; i++) {
        arr[i] = rand() % 100;
        printf("%d ", arr[i]);
    }
    printf("\n\n");

    int segment_size = N / SEGMENTS;
    double start = omp_get_wtime();

    // Step 1: Parallel sort segments
    #pragma omp parallel for num_threads(SEGMENTS) ordered
    for (int s = 0; s < SEGMENTS; s++) {
        int left = s * segment_size;
        int right = left + segment_size - 1;
        mergesort(arr, left, right);

        // Print each sorted segment in order
        #pragma omp ordered
        {
            printf("Sorted Segment %d: ", s + 1);
            for (int i = left; i <= right; i++)
                printf("%d ", arr[i]);
            printf("\n");
        }
    }

    // Step 2: Merge segments sequentially (can also be parallelized for large N)
    int left1 = 0;
    int right1 = segment_size - 1;
    for (int s = 1; s < SEGMENTS; s++) {
        int left2 = s * segment_size;
        int right2 = left2 + segment_size - 1;
        merge_segments(arr, left1, right1, left2, right2);
        right1 = right2; // Update right boundary for merged array
    }

    double end = omp_get_wtime();

    // Step 3: Print fully sorted array
    printf("\nFully sorted array:\n");
    for (int i = 0; i < N; i++)
        printf("%d ", arr[i]);
    printf("\n");

    printf("\nTotal Execution time: %f seconds\n", end - start);

    return 0;
}
