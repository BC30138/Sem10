#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно
#include <syslog.h> // для работы с журналом
#include <signal.h> // для работы с сигналами
#include <dirent.h> // для работы с файловой системой
#include <string.h>
#include <time.h>
#include "../tools/tools.h"

char * dir_path;
int recheck_time;
FILE *config_file;
char *config_path;

void read_config(){
    char * strtime;
    size_t path_len = 0;
    size_t strtime_len = 0;

    config_file = fopen(config_path, "r");
    if (config_file == NULL) {
        syslog(LOG_ERR, "config file not found: path to config should be as argument");
        exit(EXIT_FAILURE);
    }

    if (getline(&dir_path, &path_len, config_file) == -1) {
        syslog(LOG_ERR, "config file formatting is incorrect");
        exit(EXIT_FAILURE);
    }

    if (getline(&strtime, &strtime_len, config_file) == -1) {
        syslog(LOG_ERR, "config file formatting is incorrect");
        exit(EXIT_FAILURE);
    }

    char *tmp;
    size_t len = 0;
    if (getline(&tmp, &len, config_file) != -1) {
        syslog(LOG_ERR, "config file formatting is incorrect");
        exit(EXIT_FAILURE);
    }

    recheck_time = atoi(strtime);
    strtok(dir_path, "\n");

    fclose(config_file);
}

void signal_handler(int sig) {
    switch (sig)
    {
        case SIGHUP:
            read_config();
            syslog(LOG_WARNING, "config file updating complete");
            break;
        case SIGTERM:
            syslog(LOG_WARNING, "daemon terminated");
            exit(0);
            break;
    }
}

void run_task_2(char *argv[]) {

    daemonize_();

    openlog("task2daemon", 0, LOG_USER);
    // работа с содержимым конфига
    DIR *dir;
    struct dirent *entry;
    struct stat file_stat;

    config_path = argv[1];
    read_config();
    signal(SIGTERM, signal_handler);
    signal(SIGHUP, signal_handler);
    while(1){
        dir = opendir(dir_path);
        while ((entry = readdir(dir)) != NULL) {
            if ((strcmp(entry->d_name, ".") != 0)
                    && (strcmp(entry->d_name, "..") != 0)) {
                char *file_path = malloc(strlen(dir_path)
                                    + strlen(entry->d_name) + 2);
                strcpy(file_path, dir_path);
                strcat(file_path, "/");
                strcat(file_path, entry->d_name);
                stat(file_path,  &file_stat);
                if ((time(NULL) - file_stat.st_mtime) < recheck_time ) {
                    syslog(LOG_NOTICE,
                     "content of folder modified in file: %s", entry->d_name);
                }
            }
        }
        closedir(dir);
        sleep(recheck_time);
    }
}