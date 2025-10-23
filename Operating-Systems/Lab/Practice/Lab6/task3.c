#include <stdio.h>
#include <fcntl.h>    // for open()
#include <unistd.h>   // for read(), close()
#include <ctype.h>    // for isspace()
#include <string.h>

int main() {
    char filename[50];
    char buffer[1024];
    int fd, bytesRead;
    int lines = 0, words = 0, chars = 0;
    int inWord = 0;

    printf("Enter the filename: ");
    scanf("%s", filename);

    // ---------------- Using System Calls ----------------
    fd = open(filename, O_RDONLY);
    if (fd == -1) {
        printf("Error opening file using system call!\n");
        return 1;
    }

    while ((bytesRead = read(fd, buffer, sizeof(buffer))) > 0) {
        for (int i = 0; i < bytesRead; i++) {
            chars++;  // count every character

            if (buffer[i] == '\n')
                lines++;

            if (isspace(buffer[i]))
                inWord = 0;
            else if (inWord == 0) {
                inWord = 1;
                words++;
            }
        }
    }

    close(fd);

    printf("\n--- Using System Calls ---\n");
    printf("Lines: %d\nWords: %d\nCharacters: %d\n", lines, words, chars);

    // ---------------- Using fprintf (High-Level I/O) ----------------
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("Error opening file using fopen!\n");
        return 1;
    }

    lines = words = chars = 0;
    inWord = 0;
    char ch;

    while ((ch = fgetc(fp)) != EOF) {
        chars++;

        if (ch == '\n')
            lines++;

        if (isspace(ch))
            inWord = 0;
        else if (inWord == 0) {
            inWord = 1;
            words++;
        }
    }

    fprintf(stdout, "\n--- Using fprintf/fgetc ---\n");
    fprintf(stdout, "Lines: %d\nWords: %d\nCharacters: %d\n", lines, words, chars);

    fclose(fp);
    return 0;
}
