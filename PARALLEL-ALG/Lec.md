# Лекция №1. 13.02.2019
## Java Memory Model.

Модель памяти - способ доступа к памяти, а именно как система (параллельная или последовательная) работает с ней.

Java Concurrency in Practice - очень понятная книга.

JSR 133 - стандарт организации модели памяти. 

Зачем нужен стандарт:
- Чтобы программист понимал как устроена память, что можно делать, а что нет.

Бывает два типа моделей памяти: 
1. Сильная модель памяти.

    все процессоры всегда видят одинаковые значения для любой заданной ячейки памяти.

2. Слабая модель памяти.

    требуются специальные инструкции - барьеры памяти, требуются для сброса или объявления недействительными данных в ячейке.

ccNUMA - память общая для процессоров, но доступ к памяти зависит от расположения памяти (на работающем ядре, на сокете в другом ядре, в ядре на другом сокете), при этом когерентность обеспечивается аппаратно. тип памяти поддерживает ОС Linux, используя библиотеки libnuma, afinity (не допускает "переезда" потока на другое ядро, в случае чего память станет нелокальной).

Видимость - если поток работает с данными и выгрузил значения полей к себе в локальную память, после чего изменил значения полей, то другой поток может не увидеть изменений.

Reordering - для увеличения производительности процессор/компилятор могут переставлять местами некоторые инструкции/операции, что может привести к к проблемам: 

```cpp
//first thread
result = calc(); //    если переставить местами эти две строки 
resultReady = true; // получится ошибка

//second thread
if (resultReady) takeDesision(result);
```

Happens before - в JMM введена данная абстракция. Она означает, что если операция X связана отношением happens-before с Y, то обязательно выполнится сначала X, потом Y. (Используются мониторы)

В лекции приведен список операций happens-before, который необходимо понять для хорошего параллельного программирования.

# Лекция №3 19.03.19
Классификация Флинна, закон Амдала и пр. надо вспомнить.

Разделяемая (одна память - много процессоров) и распределенная память (для каждого процессора своя память) .

Кластер - это набор независимых вычислителей, объединенных в одну систему.

Сетевые топологии. 

- Bandwidth, 
- latency, 
- diameter of network, 
- on bisecting the network.
  - bisection width
  - bisection bandwidth

Существует множество топологий: шины, ольца, тор, гиперкубы, деревья и т.д.

Самое популярное ныне - Fat Tree (толстое дерево). Как правило 2 узла к одному каналу связи.

### Работа с СКЦ.

Существуют разные планировщики для СК. 

Алгоритм работы с суперкомпьютером: 
-  получить логин и ключ у администратора.
-  начать удаленную сессию
-  scp чтобы загружать и выгружать данные

когда мы ставим свою задачу начинает работу планировщик задач.

[Регистрация пользователя в СКЦ](http://scc.spbstu.ru/index.php/for-users/registration)

```bash
$ sinfo # узнать о очередях
$ salloc -N 1 -p tornado-K40 -A sccg1 # получить в пользование 1 узел. sccg1 - это группа
$ squeue # узнать, что нам выделено
$ srun -N 1 -p tornado-K40 -A sccg1 <команда/скрипт> # он пробовал ls. не до конца ясно 
$ sbatch -N 2 -p tornado-K40 -A sccg1 script.sh # поставить в очередь задачу
```

если требуется специфические библиотеки, версии компиляторов и т.д.

надо использовать команду для подгрузки софта, которые есть в директории */opt/software/*. script.sh:
```bash
#!/bin/bash

module purge # очистить загруженные модули
module load python/3.6.5 # подключаем модуль
python --version # проверка

```

основные команды: srun, scancel, sinfo, sbatch ... 

### pthreads

это один из стандартов posix.

это малость не то, но попытка переписать данный код: 

____
hello_world.c
```cpp
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *say_hi(void *arg)

int main(int argc, char* argv[] ) {
    printf("how many threads?");
    int n; scanf("%d", &n);
    {
       pthread_t t[n];
       pthread_attr_t a;
       int i,id[n];
       printf("creating %d threads", n);
       for (i = 0; i < n; i++){
            id[i] = i;
            pthread_attr_init(&a);
            pthread_create(&t[i],&a,say_hi,(void*)&i);
            // pthread_create(&t[i],&a,say_hi,(void*)&id[i]);
       }
       printf("waiting for threads to return ...\n");
       for(i = 0; i < n; i++) pthread_join(t[i],NULL);
    }
    return 0;
}

void *say_hi(void *arg) {
    int *i = (int*) arg;
    printf("hello world from thread %d!\n", *i);
    return NULL;
}
```

```bash 
gcc -l pthread hello_world.c
```

### Mutex

initialization:
```cpp
pthread_mutex_t L = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_lock(&L); // request a lock
pthtrad_mutex_unlock(&L); // release the lock
```

```bash
$ module load compiler/intel/2017.5.239
$ icc -l pthread hello_world.c
```

В качестве задания со * - Dining philosopher.

 # Лекция №4 26.03.2019

 ### MPI (Message Passing Interface)

Дома: попробовать запустить и настроить MPI на двух виртуальных машинах.

[хороший туториал по MPI](mpitutorial.dom)

```cpp
#include <mpi.h>

int main (int argc, char *argv) {
    int i, p;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &p);
    MPI_Comm_rank(MPI_COMM_WORLD, &i);

    printf("Hello world %d out of %d", i, p);

    MPI_Finalize();

    return 0;
}
```

usage:
```bash
$ salloc -N -1 -p tornado -A sccg1 
...
# подгрузить компиляторы.
$ mpicc mpi_hello_world.c
$ mpirun -np 5 a.out 
```

## Передача int

MPI_Bcast
```cpp
int n;
MPI_Bcast(&n, MPI_INT, 0, MPI_COMM_WORLD);
```

```cpp
#include <stdio.h>
#include <mpi.h>

void manager(int *n); // (scanf printf)
void worker(int i, int n); // -||- просто разные функции

int main (int argc, char *argv) {
    int myid, np, n;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &np);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);

    if (myid == 0) manager(&n);

    MPI_Bcast(&n, MPI_INT, 0, MPI_COMM_WORLD);
    // MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (myid != 0) worker(myid,n);

    MPI_Finalize();

    return 0;
}

void manager(int *n) {
    printf("Type \n");
    scanf("%d", n);
}

void worker(int i, int n) {
    printf("Node %d writes %d", i, n)
}
```

Почему-то не сработало:
```cpp
#include <stdio.h>
#include <mpi.h>

void manager(int *n); // (scanf printf)
void worker(int i, int n); // -||- просто разные функции

#define BOSS 2

int main (int argc, char *argv) {
    int myid, np, n;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &np);
    MPI_Comm_rank(MPI_COMM_WORLD, &myid);

    if (myid == BOSS) manager(&n);

    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (myid != BOSS) worker(myid,n);

    MPI_Finalize();

    return 0;
}

void manager(int *n) {
    printf("Type \n");
    scanf("%d", n);
}

void worker(int i, int n) {
    printf("Node %d writes %d", i, n)
}
```

mpi4py - mpi для питона
