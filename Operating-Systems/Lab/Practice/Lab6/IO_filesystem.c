#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

int main() {
    int fd, sz;
    char bf[13];

    // Open or create the file with read-write permissions
    fd = open("foo.txt", O_RDWR | O_CREAT, 0644);
    if (fd == -1) {
        printf("Error in file opening! errno = %d\n", errno);
        return 1;
    }

    // Write to the file
    sz = write(fd, "hello world", strlen("hello world"));
    printf("The size of data written is: %d bytes\n", sz);

    // Move file pointer back to beginning before reading
    lseek(fd, 0, SEEK_SET); // the file descriptor, no. of bytes to move, where to move from 

    // Read data back
    read(fd, bf, 12);
    bf[12] = '\0';  // null terminate the string

    printf("Data read from file: %s\n", bf);

    // Close the file
    close(fd);
    return 0;
}
