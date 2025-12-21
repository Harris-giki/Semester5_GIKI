#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"
#include "kernel/fs.h"
#include "kernel/param.h"

// Get the filename from a path (everything after the last '/')
char*
getname(char *path)
{
  char *p;

  // Find first character after last slash
  for(p = path + strlen(path); p >= path && *p != '/'; p--)
    ;
  p++;

  return p;
}

void
find(char *path, char *filename, int exec_mode, char **exec_argv, int exec_argc)
{
  char buf[512], *p;
  int fd;
  struct dirent de;  //a directory entry (contains inum and name)
  struct stat st;  //file info (type, size, inode number, etc.)

  // Open the path
  if((fd = open(path, 0)) < 0){
    fprintf(2, "find: cannot open %s\n", path);
    return;
  }

  // Get file/directory info
  if(fstat(fd, &st) < 0){
    fprintf(2, "find: cannot stat %s\n", path);
    close(fd);
    return;
  }

  switch(st.type){
  case T_FILE:
    // If it's a file, check if the name matches
    if(strcmp(getname(path), filename) == 0){
      if(exec_mode){
        // Execute command with the file as argument
        int pid = fork();
        if(pid == 0){
          // Child process
          // Build argv:  [cmd, arg1, ..., filename, 0]
          char *argv[MAXARG];
          int i;
          for(i = 0; i < exec_argc; i++){
            argv[i] = exec_argv[i];
          }
          argv[exec_argc] = path;
          argv[exec_argc + 1] = 0;

          exec(argv[0], argv);
          fprintf(2, "find: exec %s failed\n", argv[0]);
          exit(1);
        } else if(pid > 0){
          // Parent process - wait for child
          wait(0);
        } else {
          fprintf(2, "find: fork failed\n");
        }
      } else {
        printf("%s\n", path);
      }
    }
    break;

  case T_DIR:
    // Check if path is too long
    if(strlen(path) + 1 + DIRSIZ + 1 > sizeof buf){
      printf("find: path too long\n");
      break;
    }

    // Copy path to buffer and add '/'
    strcpy(buf, path);
    p = buf + strlen(buf);
    *p++ = '/';

    // Read each directory entry
    while(read(fd, &de, sizeof(de)) == sizeof(de)){
      // Skip empty entries
      if(de. inum == 0)
        continue;

      // Skip "." and ".." directories
      if(strcmp(de.name, ".") == 0 || strcmp(de.name, "..") == 0)
        continue;

      // Build the full path:  buf = path + "/" + de.name
      memmove(p, de.name, DIRSIZ);
      p[DIRSIZ] = 0;

      // Get info about this entry if less than 0 then error
      if(stat(buf, &st) < 0){
        printf("find: cannot stat %s\n", buf);
        continue;
      }

      // If the name matches, execute or print
      if(strcmp(de.name, filename) == 0){
        if(exec_mode){
          // Execute command with the file as argument
          int pid = fork();
          if(pid == 0){
            // Child process
            char *argv[MAXARG];
            int i;
            for(i = 0; i < exec_argc; i++){
              argv[i] = exec_argv[i];
            }
            argv[exec_argc] = buf;
            argv[exec_argc + 1] = 0;

            exec(argv[0], argv);
            fprintf(2, "find: exec %s failed\n", argv[0]);
            exit(1);
          } else if(pid > 0){
            // Parent process - wait for child
            wait(0);
          } else {
            fprintf(2, "find: fork failed\n");
          }
        } else {
          printf("%s\n", buf);
        }
      }

      // If it's a directory, recurse into it
      if(st.type == T_DIR){
        find(buf, filename, exec_mode, exec_argv, exec_argc);
      }
    }
    break;
  }

  close(fd);
}

int
main(int argc, char *argv[])
{
  int exec_mode = 0;
  char *exec_argv[MAXARG];
  int exec_argc = 0;

  // Minimum arguments:  find <dir> <filename>
  if(argc < 3){
    fprintf(2, "Usage: find <directory> <filename> [-exec cmd args...]\n");
    exit(1);
  }

  // Check if -exec is present
  if(argc >= 4 && strcmp(argv[3], "-exec") == 0){
    exec_mode = 1;
    // Collect all arguments after -exec as the command
    for(int i = 4; i < argc; i++){
      exec_argv[exec_argc++] = argv[i];
    }

    if(exec_argc == 0){
      fprintf(2, "find: -exec requires a command\n");
      exit(1);
    }
  }

  find(argv[1], argv[2], exec_mode, exec_argv, exec_argc);
  exit(0);
}
