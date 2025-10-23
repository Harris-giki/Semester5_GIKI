#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main()
{
    char filename[50];
    char buffer[1000];
    
    printf("Enter the filename to read: ")
    scanf("%s", filename);

    //---- using system calls ----

    int fd = open(filename, O_RDONLY);
    if(fd==-1)
    {
        printf("Error occured opening the file. \n");
        return 1;
    }

    int byteRead;
    while((byteRead = read(fd, buffer, sizeof(buffer))>0)) //reading from the file
    {
        write(1, buffer, byteRead); // 1 means output @ terminal
    }
    close(fd);

    // ---- Output using fprintf/fscanf ---

    FILE *fp = fopen(filename, "r")

    if(fp=NULL)
    {
        printf("Error opening the file")
        return 1;
    }

    char words[100];
    while(fscanf(fp, "%s", word)==1) // reading from the file
    {
        fprintf(stdout, "%s", word); // print to terminal
    }
}