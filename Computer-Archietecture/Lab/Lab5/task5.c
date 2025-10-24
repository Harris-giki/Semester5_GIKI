#include <stdio.h>
#include <omp.h>

int main() {
    int arr[100];
    int sum = 0;

    for (int i = 0; i < 100; i++)
        arr[i] = i + 1;


    #pragma omp parallel
    {
        int local_sum=0;
        #pragma omp for{
            for(int i=0; i<100; i++)
            {
                local_sum+=arr[i];
            }
            #pragma omp atomic
            sum += local_sum;
        }
    }

    }