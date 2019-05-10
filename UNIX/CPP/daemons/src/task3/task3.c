#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно
#include <syslog.h> // для работы с журналом
#include <signal.h> // для работы с сигналами
#include <dirent.h> // для работы с файловой системой
#include <string.h>
#include "../tools/tools.h"
#include <sys/socket.h>
#include <netinet/in.h>

void signal_handler_task_3(int sig) {
    switch (sig)
    {
    case SIGTERM:
        syslog(LOG_WARNING, "daemon terminated");
        exit(0);
        break;
    }
}

void run_task_3() {
    // daemonize_();
    openlog("task3daemon", 0, LOG_USER);
    syslog(LOG_DAEMON, "daemon has been started");
    signal(SIGTERM, signal_handler_task_3);


}