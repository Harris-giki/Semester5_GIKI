Great! I can provide **correct OpenMP C code examples for all 5 tasks** based on your instructions, with explanations so you can run and observe the behavior.

---

## **Task 1 – Hello World with Critical**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int num_threads = 4;

    #pragma omp parallel num_threads(num_threads)
    {
        int tid = omp_get_thread_num();
        #pragma omp critical
        {
            printf("Hello from thread %d of %d\n", tid, num_threads);
        }
    }

    return 0;
}
```

✅ **Explanation:**

* `#pragma omp critical` ensures **one thread prints at a time**, preventing mixed output.
* Run multiple times: order may vary.

---

## **Task 2 – Vector Sum with Reduction**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int arr[10] = {1,2,3,4,5,6,7,8,9,10};
    int sum_seq = 0, sum_par = 0;

    // Sequential sum
    double t1 = omp_get_wtime();
    for(int i = 0; i < 10; i++)
        sum_seq += arr[i];
    double t2 = omp_get_wtime();
    printf("Sequential sum = %d, Time = %f\n", sum_seq, t2 - t1);

    // Parallel sum with reduction
    t1 = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum_par)
    for(int i = 0; i < 10; i++)
        sum_par += arr[i];
    t2 = omp_get_wtime();
    printf("Parallel sum = %d, Time = %f\n", sum_par, t2 - t1);

    return 0;
}
```

✅ **Explanation:**

* `reduction(+:sum_par)` prevents race conditions.
* Both sums are the same. For large arrays, parallel is faster.

---

## **Task 3 – Min & Max of Array**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int arr[20] = {12, 5, 8, 22, 17, 3, 14, 19, 7, 11, 6, 2, 20, 1, 18, 15, 9, 4, 16, 10};
    int minVal, maxVal;

    // Version A – Reduction
    minVal = arr[0]; maxVal = arr[0];
    #pragma omp parallel for reduction(min:minVal) reduction(max:maxVal)
    for(int i = 0; i < 20; i++) {
        if(arr[i] < minVal) minVal = arr[i];
        if(arr[i] > maxVal) maxVal = arr[i];
    }
    printf("Reduction Min = %d, Max = %d\n", minVal, maxVal);

    // Version B – Critical
    int minC = arr[0], maxC = arr[0];
    #pragma omp parallel for
    for(int i = 0; i < 20; i++) {
        #pragma omp critical
        {
            if(arr[i] < minC) minC = arr[i];
            if(arr[i] > maxC) maxC = arr[i];
        }
    }
    printf("Critical Min = %d, Max = %d\n", minC, maxC);

    return 0;
}
```

✅ **Explanation:**

* Reduction is faster and avoids thread blocking.
* Critical also works but may slow down performance.

---

## **Task 4 – Shared Variable Update with Critical**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int counter = 0;

    // Without critical
    #pragma omp parallel num_threads(8)
    {
        counter++; // Race condition
    }
    printf("Counter without critical = %d\n", counter);

    // Reset counter
    counter = 0;

    // With critical
    #pragma omp parallel num_threads(8)
    {
        #pragma omp critical
        counter++;
    }
    printf("Counter with critical = %d\n", counter);

    return 0;
}
```

✅ **Explanation:**

* Without critical → final counter may be < 8 (race condition).
* With critical → final counter = 8 (correct).
* Serialization slows execution because threads must wait their turn.

---

## **Task 5 – Matrix Multiplication with OpenMP**

```c
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 200  // Size of matrices

int main() {
    int **A = malloc(N * sizeof(int*));
    int **B = malloc(N * sizeof(int*));
    int **C = malloc(N * sizeof(int*));
    for(int i=0;i<N;i++){
        A[i]=malloc(N*sizeof(int));
        B[i]=malloc(N*sizeof(int));
        C[i]=malloc(N*sizeof(int));
    }

    // Initialize matrices
    for(int i=0;i<N;i++)
        for(int j=0;j<N;j++){
            A[i][j] = i+j;
            B[i][j] = i*j;
            C[i][j] = 0;
        }

    double start = omp_get_wtime();

    #pragma omp parallel for
    for(int i=0;i<N;i++){
        for(int j=0;j<N;j++){
            int sum = 0;
            for(int k=0;k<N;k++)
                sum += A[i][k]*B[k][j];
            C[i][j] = sum;
        }
    }

    double end = omp_get_wtime();
    printf("Matrix multiplication completed in %f seconds\n", end - start);

    // Free memory
    for(int i=0;i<N;i++){
        free(A[i]); free(B[i]); free(C[i]);
    }
    free(A); free(B); free(C);

    return 0;
}
```

✅ **Explanation:**

* Parallelizes **outer loop over rows**.
* Each thread calculates a row independently.
* Reduction is not needed here because each thread writes to its own row.
* Run with different thread counts to see speedup.

---

These programs cover **all your tasks** and illustrate the **correct use of OpenMP**: `critical`, `atomic`, and `reduction`.

---

I can also create a **single combined file** where you can **run all 5 tasks one after another** with clear separation and timing, if you want.

Do you want me to do that?
