omp_get_thread_num()
• Returns the ID of the current thread.
• Master thread has ID = 0.
Example:
int id = omp_get_thread_num();
printf("I am thread %d\n", id);
❖ omp_get_num_threads()
Returns the total number of threads in the parallel region.
Example:
int total = omp_get_num_threads();
printf("We are %d threads working together\n", total);
❖ omp_set_num_threads(n)
Manually sets the number of threads to n for the next parallel region.
Example:
omp_set_num_threads(4);
#pragma omp parallel
printf("Thread %d is working\n", omp_get_thread_num());
{
}
❖ Environment Variable: export OMP_NUM_THREADS=n
Another way to control the number of threads (from the terminal).
Example:
export OMP_NUM_THREADS=2
gcc -fopenmp hello.c -o hello
./hello
❖ omp_get_num_procs()
Returns the number of processors (CPU cores) available.
Example:
printf("This system has %d processors\n", omp_get_num_procs());
❖ omp_get_dynamic()
Returns whether dynamic adjustment of thread count is enabled (1 = true, 0 = false).