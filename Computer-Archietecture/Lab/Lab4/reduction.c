#include <stdio.h>
#include <omp.h>

int main() {
    int sum = 0;

    #pragma omp parallel for reduction(+:sum)
    for(int i = 0; i < 100; i++) {
        sum += i;
    }

    printf("The sum calculated is: %d\n", sum);
    return 0;
}
