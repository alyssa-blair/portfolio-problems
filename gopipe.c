/* gopipe.c
 *
 * Execute up to four instructions with up to 8 commands, piping the output of each into the
 * input of the next.
 * 
 */

#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <wait.h>
#include <stdio.h>

void prompt_user();
struct dict read_data(char[80], int, struct dict);
struct dict add_to_dict(char *, char *[], int, struct dict);
void execute_instr(struct dict, int);


struct dict {
    char command[4][80];
    char args[4][8][80];
    int argCount[8];
} dict;


void prompt_user() {
    // prompts the user for input and passes it to the functions to be sorted
    int n;
    int count = 0;
    struct dict data;
    char buffer[80];
    
    while ((n = read(0, buffer, 80)) > 1) {
        data = read_data(buffer, count, data);
        if (count == 3) {
            // reached the maximum number of instructions 
            count++;
            break;
        }
        count++;
        
        // reset the buffer
        memset(buffer, 0, sizeof(buffer));
    }
    
    execute_instr(data, count);
}


struct dict read_data(char buffer[80], int count, struct dict data) {
    // parses through the lines splitting them into arguments and commands
    
    // split the current line into commands and arguments
    char *line = strtok(buffer, "\n");
    strtok(line, " ");
    char *command = line;
    char *args[8];
    memset(args, 0, sizeof(args));
    
    int i = 0;
    while (line != NULL) {
        line = strtok(NULL, " \n");
        args[i] = line;
        i++;
    }
    
    return add_to_dict(command, args, count, data);
}

struct dict add_to_dict(char *command, char *args[], int count, struct dict data) {
    // takes the passed arguments and commmand and adds them to a structure
    // returns the structure
    
    
    int argCount = 0;
    
    for (int i = 0; i < 8; i++) {
        if (args[i] == NULL)
            break;
        // add each of the arguments to the dictionary
        strcat(data.args[count][i], args[i]);
        argCount++;
    }
    
    // assign the command
    strcpy(data.command[count], command);
    data.argCount[count] = argCount;
    return data;
}

void execute_instr(struct dict data, int count) {
    // creates pipes and child processes and executes instructions through them
    char *env[] = {0};
    int fd[count][2];
    int pid[4];
    
    
    for (int c = 0; c < count; c++) {
            char *args[data.argCount[c] + 2];
            args[data.argCount[c] + 1] = 0;
            char command[80];
        
            for (int k = 1; k < data.argCount[c] + 1; k++) 
                 args[k] = data.args[c][k-1];
            
            strcpy(command, data.command[c]);
            args[0] = data.command[c];

        // not the first or last command
        if (c != 0 && c != count - 1) {
                pipe(fd[c]);
            
                // fork failed, exit
                if ((pid[c] = fork()) < 0)
                   exit(1);
                if (pid[c] == 0) {
                    // child process
                    dup2(fd[c-1][0], 0);
                    dup2(fd[c][1], 1);
                    
                    // close the ends of the pipe and send executed command through
                    close(fd[c][0]);
                    close(fd[c-1][1]);
                    execve(command, args, env);
                    exit(0);
                    
                } else {
                    // parent process
                    close(fd[c][1]);
                }
            
            } else if (c == count - 1) {
                // last command

                // fork failed, exit
                if ((pid[c] = fork()) < 0)
                    exit(1);
                
                if (pid[c] == 0) {
                    // child process
                    dup2(fd[c-1][0], 0);
                    
                    // close one end of the pipe and execute hte last instruction
                    close(fd[c-1][1]);

                    execve(command, args, env);
                    
                } else {
                    // parent process
                    close(fd[c-1][1]);
                }
            
                // wait for all the children
                for (int w = 0; w < count; w++)
                    waitpid(pid[w], NULL, 0);
            
            } else {
                // first command
                pipe(fd[c]);
                
                // fork failed, exit
                if ((pid[c] = fork()) < 0) 
                    exit(0);
                
                if (pid[c] == 0) {
                    // child process
                    dup2(fd[c][1], 1);
                    close(fd[c][0]);
                    
                    // close one end of the pipe and send instruction through
                    execve(command, args, env);
                } else {
                    // parent process
                    close(fd[c][1]);
                }
           
            }

        }
}



int main() {
    prompt_user();
}

