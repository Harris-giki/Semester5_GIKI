#include <stdio.h>
#include <stdlib.h>

int main()
{
    int n , i, *ptr, sum = 0;

    printf("Enter a number of elements: ");
    scanf("%d", &n);

    ptr = (int* ) malloc (n* sizeof(int));

    if(ptr == NULL)
    {
        printf("Error! Memory not allocated");
        exit(0);
    }

    printf("Enter the elements: ");
    for(int i = 0; i<n; i++)
    {scanf("%d", ptr+i);
    sum += *(ptr + i);}

    printf("The sum is: %d", sum);

    free(ptr);
    return 0;
}