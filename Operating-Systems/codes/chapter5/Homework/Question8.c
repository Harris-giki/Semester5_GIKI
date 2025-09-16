#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int fd[2]; // pipe file descriptors
    pid_t pid1, pid2;

    // create the pipe
    if (pipe(fd) < 0) {
        perror("pipe failed");
        exit(1);
    }

    // first child: writes into pipe (like "ls")
    pid1 = fork();
    if (pid1 < 0) {
        perror("fork failed");
        exit(1);
    }
    else if (pid1 == 0) {
        // child 1
        close(fd[0]);              // close unused read end
        dup2(fd[1], STDOUT_FILENO); // redirect stdout to pipe
        close(fd[1]);              // close original write end
        execlp("ls", "ls", "-l", NULL); // run "ls -l"
        perror("execlp failed");
        exit(1);
    }

    // second child: reads from pipe (like "wc -l")
    pid2 = fork();
    if (pid2 < 0) {
        perror("fork failed");
        exit(1);
    }
    else if (pid2 == 0) {
        // child 2
        close(fd[1]);              // close unused write end
        dup2(fd[0], STDIN_FILENO); // redirect stdin from pipe
        close(fd[0]);              // close original read end
        execlp("wc", "wc", "-l", NULL); // run "wc -l"
        perror("execlp failed");
        exit(1);
    }

    // parent process
    close(fd[0]);
    close(fd[1]); // close both ends in parent
    wait(NULL);   // wait for first child
    wait(NULL);   // wait for second child

    return 0;
}
