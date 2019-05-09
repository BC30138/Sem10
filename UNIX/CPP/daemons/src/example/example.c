#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/types.h> // для того, чтобы избежать недопониманий с интеллисэнс
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно
#include <syslog.h> // для работы с журналом
#include <signal.h> // для работы с сигналами
#include <dirent.h> // для работы с файловой системой
#include <string.h>
#include <time.h>
#include "../tools/tools.h"

void signal_handler_example(int sig) {
    switch (sig)
    {
        case SIGHUP:
            syslog(LOG_WARNING, "Center! Target is down! terminal is killed.");
            break;
        case SIGINT:
            syslog(LOG_WARNING, "it should be stoped...");
            exit(0);
            break;
    }
}

void syslog_example() {
    openlog("exampleprog", 0, LOG_LOCAL0);
    syslog(LOG_NOTICE, "Priv Che Del. Ya %d", getuid());
    closelog();
}

void simple_daemon_example() {
    daemonize_();
    signal(SIGINT, signal_handler_example);
    signal(SIGHUP, signal_handler_example);
    while(1){
        sleep(10);
    }
}

