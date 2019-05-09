#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/types.h> // для того, чтобы избежать недопониманий с интеллисэнс
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно

void daemonize_() {
    pid_t process_id, session_id;
    process_id = fork(); // отделяемся от родительского процесса

    // убедиться, что мы отделились
    if (process_id < 0) exit(EXIT_FAILURE);

    umask(0); // изменение файловой маски

    session_id = setsid(); // получаем идентификатор сессии
    if (session_id < 0) {
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