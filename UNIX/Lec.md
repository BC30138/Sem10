# Лекция №1
## 12.02.19
### История

Multics (MIT, GE, Bell Labs). Разработка начата в 1964 году.

UNIX как таковая система исчезла почти, но UNIX-подобные применяются повсеместно. 

1969 - Bell Labs выходят из Multics. Начинается разработка UNICS. В дань моде далее переименована в UNIX. 

1970 - первая реализация UNICS для PDP-7 (День рождения UNIX, системное время отсчитывается от этой даты).

1971 - реализация для PDP-11.

Реализация была не на си, как бы на ассемблере. Портирование системы затруднено.

1973 - Денис Ритчи предлагает переписать UNIX на языке B (предшественник Си). В ходе этого рождается язык Си. Как результат получилась переносимая между различными архитектурами ОС, где только около 10% (магическая константа, такое количество кода всегда есть) было написано на ассемблере.

1978 - Раскол на BSD UNIX, созданного в университете Беркли и System V от AT&T. Произошел он из-за реализации TCP/IP

1983 - Ричард Столлман объявил о создании проекта GNU - свободной UNIX-подобной операционной системы с нуля, без использования оригинальных исходников.

1984 - что-то вроде первой графической оболочки. X Window.

1991 - в проекте GNU были доступны все основные компоненты операционной системы: GNU toolchain, glibs, coreutils и т.д. Однако не было самого ядра.

1992 - судебный иск против BSD Unix от UNIX Systems Laboratories (Bell Labs) связанный с выходом 386/BSD. 

1994 - Спорный код был переписан. BSD 4.4

1995 - SCO приобретает права на UNIX.

2000 - SCO продает UNIX-бизнес. Некоторые говорят, что UNIXwave была последней околоюникс системой.

"Just for fun" Линус Торвальдс - это биография, говорят прикольнАА.

Торвальдсу не нравился терминал - он его переписывал долго и так система получилась.

17 сентября 1991 - выложен исходный код freax (x - потому что модна) под лицензией GPL.

Человек, который выложил для Торвальдса систему в открытый доступ, но положил в папку с названием Linux (x - МОДААА), поэтому все назвали это Linux.

1993 - вышел дистрибутив один из первых дистрибутивов Linux Slackware. В этом же году чуть позже вышли дистрибутивы от RedHat и Debian.

1994 - выход версии 1.0 Linux.

1988 - создание первой версии GNU GPL (General Public License).

1998 - раскол в сообществе СПО. Эрик Реймонд основал OSI (Open Source Initiative). Раскол возник в основном из-за неоднозначности трактовки слова "free" в английском языке.

2007 - создание LGPL (Lesser GPL). Загвоздка в libc, ей нужны исходники и в этой лицензии оговорено, что можете менять все подряд и не показывать исходники, но нельзя менять такие библиотеки как libc, если их изменили, то должны показать исходники. 

[Здесь про локализацию и все такое, пропустил]

POSIX (Portable Operating System Interface for Unix) - набор стандартов, описывающих интерфейсы между ОС и прикладной программой. Самый важные стандарты POSIX 1003.1, 1003.2, 1003.1b, 1003.1c.

X/Open XPG - консорциум

LSB - проект по стандартизации дистрибутивов Linux. То, что не описал POSIX: уровни запуска, стандартные библиотеки, система печати, иерархия файловой системы и расширения к X Window System.

А также для иерархии файлов стандарт FHS. 

[ЗДЕСЬ ДОЛЖНО БЫТЬ ИЗОБРАЖЕНИИ ИЗ ЛЕКЦИИ, ПОКАЗЫВАЮЩАЯ СТАНДАРТ СТРОЕНИЯ АРХИТЕКТУРЫ ЮНИКС-ПОДОБНЫХ]

Задание на семестр:

Ребят, которые из Политеха, покарали за то что они такие - задание в именных пдфках.

А у чотких посанов прибывших будут появляться задания на: скрипты, демон-процессы, серверы.

# Лекция №2 26.02.19

```
$ command -x_1 [-x_2 args] {-x_n | --long-options} args ... \n
```

в документации к команде как правило пишут [] если это обязательный аргумент, а {} для опциональных, конец команды как правило перенос строки.

поток вывода >

```
find /proc >res.txt 2>err.txt
```

это мы выведем положительно результаты поиска (не отказано в доступе) в файл res.txt, а отрицательный в файл err.txt

```
find /proc >res.txt 2>&1
```

не пересоздает файл: >>

Здесь мы запишем все в один файл. &1 - значит использовать первый поток.

поток ввода <

/dev/null - туда отправляются данные, но не возвращаются

```
find /proc 2>/dev/null > | grep 22886
```

тут мы ошибки отправили в никуда и вывели поиск 22886.

Переменные (по сути всегда строки)
```
$ NAME=ls
$ $NAME
```

сработает команда ls

```
$ NAME=user
$ echo {$NAME}777
user777
```

Подстановка результата работы команды в аргументы другой команды: 

```
$ grep 2 `cat file.txt`
```

В файле "file.txt" содержится список файлов. Таким образом мы найдем все 2 в файлах из списка "file.txt".

включить режим отладки:
```
$ set -x
```

выключить режим отладки:

```
$ set +x
```

так же вместо ``  можно использовать $(). это полезно в случае $( $() )

~ - это переменная HOME.

выражения: 
```
$ i=$[1 + 699]
$ echo $i
700
```

если надо вещественные числа, то калькулятор
```
$ i=`echo 1.9 + 0.2 | bc -l`
$ echo $i
2.1
```

```
$ i=$((1 + 699))
$ echo $i
1 + 699
```

```
$ echo I have 666
I have 666
$ echo I have 666$
I have 666$
$ echo I have 666$i
I have 6661 + 699
$ echo "I have 666$i"
I have 666$((1 + 699))
```

комбинация команд

1 потом 2

```
$ stat file.txt ; cat file.txt
```

2 выполнится если 1 вернула 0(выполнилась успешно).

```
$ stat file.txt && cat file.txt
```

2 выполнится если 1 вернула 1(провалилась).

```
$ stat file.txt || cat file.txt
```

Проверка существования файла (сложноватая)
```
$ stat fillll.txt 2>/dev/null || echo File NOT EXIST
```

лучше конечно так:
```
$ test fillll.txt
$ echo $?
0
$ test file.txt
$ echo $?
1
$ test 7 -le 9
$ echo $?
1
```

# Лекция №3 5.03.19
## Простейший скрипт

Работа со скриптом:

```sh
$ ./script.sh John Bill Michael
$ ./script.sh
```

Скрипт:

```sh
#!/bin/bash

echo $0 $1 $2 $3

TEMP=$1

if test -z TEMP
then 
    echo Hello World
else 
    echo Hello $1
fi
```

```sh
#!/bin/bash

echo $@

if test $# -eq 0
then 
    echo Hello World
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```sh
#!/bin/bash

if [ $# -eq 0 ]
then 
    echo Hello World
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```sh
#!/bin/bash

if test $# -eq 0
then 
    echo Hello World
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```sh
#!/bin/bash

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```sh
#!/bin/bash

j=0

while test $j -lt 100
do 
    echo $j
    j=$((j + 1))
    # j=$(($j + 1))
done
exit

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```
$ ./script.sh -h
$ ./script.sh --help
$ ./script.sh -a
$ ./script.sh -l
$ ./script.sh -abc
```

```sh
#!/bin/bash

case $1 in
    -h|--help) echo Usage $0 enter list with names
    -[la]) echo $1 typed
    *) echo Unknown parameter $1

exit

j=0

while test $j -lt 100
do 
    echo $j
    j=$((j + 1))
    # j=$(($j + 1))
done
exit

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```bash
$ ./script.sh A B C
```


```bash
#!/bin/bash

echo $1 $2

shift

echo $1 $2

exit

function get_help() 
{
    case $1 in
        -h|--help) echo Usage $0 enter list with names
        -[la]) echo $1 typed
        *) echo Unknown parameter $1
}

get_help() $@

exit

j=0

while test $j -lt 100
do 
    echo $j
    j=$((j + 1))
    # j=$(($j + 1))
done
exit

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

Теперь что-то в терминале:
```sh
$ mkdir 1 2 3 4 5 6 7
```

```bash
#!/bin/bash

RESULT=`find . -type d`

for i in $RESULT
do
    echo Found $i
done

exit 

echo $1 $2

shift

echo $1 $2

exit

function get_help() 
{
    case $1 in
        -h|--help) echo Usage $0 enter list with names
        -[la]) echo $1 typed
        *) echo Unknown parameter $1
}

get_help() $@

exit

j=0

while test $j -lt 100
do 
    echo $j
    j=$((j + 1))
    # j=$(($j + 1))
done
exit

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```

```sh
$ mkdir "666\ 999"
$ ./script.sh
```

Решение проблемы:

```bash
#!/bin/bash

IFS=$'\n'

RESULT=`find . -type d`

for i in $RESULT
do
    echo Found $i
done

exit 

echo $1 $2

shift

echo $1 $2

exit

function get_help() 
{
    case $1 in
        -h|--help) echo Usage $0 enter list with names
        -[la]) echo $1 typed
        *) echo Unknown parameter $1
}

get_help() $@

exit

j=0

while test $j -lt 100
do 
    echo $j
    j=$((j + 1))
    # j=$(($j + 1))
done
exit

NAMES="Petr Nikolay Vasiliy"

if test $# -eq 0
then 
    for it in $NAMES
    do
        echo Hello $it
    done
else 
    for it in $@
    do
        echo Hello $it
    done
fi
```