Perfect! I can provide **ready-to-run OpenMP C code** for all 5 lab tasks, with comments explaining shared vs private variables, barriers, atomic updates, master thread, and parallel array summation.

---

## **Task 1 – Private vs Shared Variable Demonstration**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int x = 10;

    // Private variable example
    #pragma omp parallel num_threads(4) private(x)
    {
        x = omp_get_thread_num() * 10; // Each thread has its own copy
        printf("Private x in thread %d = %d\n", omp_get_thread_num(), x);
    }

    // Shared variable example
    x = 10; // reset
    #pragma omp parallel num_threads(4) shared(x)
    {
        #pragma omp atomic
        x += 5; // Each thread increments the same x
    }

    printf("Final shared x = %d\n", x);

    /*
    Comment:
    - Private: Each thread has its own copy; changes do not affect others.
    - Shared: All threads access the same variable; must synchronize for safe updates.
    */

    return 0;
}
```

---

## **Task 2 – Barrier Demonstration**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel num_threads(4)
    {
        int tid = omp_get_thread_num();
        printf("Thread %d reached before barrier\n", tid);

        #pragma omp barrier

        printf("Thread %d passed barrier\n", tid);
    }
    return 0;
}
```

✅ **Explanation:**

* All threads wait at the barrier before continuing.
* Order before/after barrier may vary.

---

## **Task 3 – Atomic Counter**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int counter = 0;

    // Without atomic (race condition)
    #pragma omp parallel num_threads(16)
    {
        for(int i=0; i<100; i++)
            counter++; // unsafe
    }
    printf("Counter without atomic = %d (likely wrong)\n", counter);

    // Reset counter
    counter = 0;

    // With atomic
    #pragma omp parallel num_threads(16)
    {
        for(int i=0; i<100; i++)
            #pragma omp atomic
            counter++; // safe
    }
    printf("Counter with atomic = %d (correct)\n", counter);

    return 0;
}
```

---

## **Task 4 – Master Thread Logging**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    #pragma omp parallel num_threads(8)
    {
        #pragma omp master
        {
            printf("Master: Starting work\n");
        }

        // Dummy work
        int tid = omp_get_thread_num();
        printf("Thread %d doing work\n", tid);

        #pragma omp master
        {
            printf("Master: All work done\n");
        }
    }
    return 0;
}
```

✅ **Explanation:**

* Only the master thread (thread 0) executes the `master` sections.
* All threads do the dummy work.

---

## **Task 5 – Parallel Array Summation**

```c
#include <stdio.h>
#include <omp.h>

int main() {
    int arr[100];
    for(int i=0; i<100; i++)
        arr[i] = i + 1;

    // Method A: Shared sum with atomic
    int sumA = 0;
    #pragma omp parallel for
    for(int i=0; i<100; i++)
        #pragma omp atomic
        sumA += arr[i];
    printf("Method A - Final sum = %d\n", sumA);

    // Method B: Private partial sums per thread
    int sumB = 0;
    #pragma omp parallel
    {
        int local_sum = 0;
        #pragma omp for
        for(int i=0; i<100; i++)
            local_sum += arr[i];

        printf("Thread %d partial sum = %d\n", omp_get_thread_num(), local_sum);

        #pragma omp atomic
        sumB += local_sum;
    }
    printf("Method B - Final sum = %d\n", sumB);

    return 0;
}
```

✅ **Explanation:**

* Method A: simple atomic addition for shared sum.
* Method B: each thread computes its local sum, then safely adds to global sum.
* Thread-wise partial sums are printed.

---

These 5 programs cover **private vs shared, barrier, atomic, master, and parallel summation**, and can be run individually to observe behavior.

---

If you want, I can **combine all 5 tasks into a single program** with clear section separators and runtime prompts, so you can run everything at once for your lab.

Do you want me to do that?
