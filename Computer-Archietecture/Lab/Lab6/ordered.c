#include <stdio.h>
#include <omp.h>
int main() {
omp_set_num_threads(4); // fixed number of threads
printf("Without ordered:\n");
#pragma omp parallel for
for (int i = 0; i < 10; i++) {
printf("Iteration %d executed by thread %d\n", i,
omp_get_thread_num());
}
printf("\nWith ordered:\n");
#pragma omp parallel for ordered num_threads(4)
for (int i = 0; i < 10; i++) {
// do some computation
#pragma omp ordered
{
printf("Iteration %d executed by thread %d\n", i,
omp_get_thread_num());
}
}
return 0;
}