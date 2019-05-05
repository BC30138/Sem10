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

void daemonize_() {
    pid_t process_id, session_id;
    process_id = fork(); // отделяемся от родительского процесса

    // убедиться, что мы отделились
    if (process_id < 0) exit(EXIT_FAILURE);
    else exit(EXIT_SUCCESS);

    umask(0); // изменение файловой маски

    // где-то тут мы открываем логи, журналы и все такое

    session_id = setsid(); // получаем идентификатор сессии
    if (session_id < 0) {
        // здесь можно вывести в журнал информацию о сбое
        exit(EXIT_FAILURE);
    }

    // изменяем текущий каталог на тот, который точно не удалят и ничего с ним не станет
    if ((chdir("/")) < 0) { // функция chdir возвращает -1, если что-то пошло не так
        exit(EXIT_FAILURE);
    }

    // так как демон не использует терминал, то стандартные файловые дескрипторы излишни
    // и создают угрозу безопасности
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
}

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

