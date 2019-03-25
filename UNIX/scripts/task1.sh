#!/bin/bash

error_func () {
    echo Error: Incorrect arguments. Type -h to get help.
    exit 1
}

usage="$(basename "$0") 
    Something like smart search

    Usage: 
        $(basename "$0") <directory> <date>     search files in <directory> not newer then <date>. 
                                        Where <date> should have format dd/mm/yyyy.
    
    Options:
        -h --help       show this help text"

case $1 in
    -h|--help) 
        if [ $# -ne 1 ]; then 
            error_func 
        fi
        echo "$usage" 
        exit 
        ;;
    *) 
        if [ $# -ne 2 ]; then 
            error_func 
        fi
        
        if [ ! -d "$1" ]; then
            echo Error: Search directory should exist.
            exit 1
        fi
        ;;
esac

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
IFS='/' read -ra datearray <<< "$2" 
date=${datearray[2]}"-"${datearray[1]}"-"${datearray[0]}

mkdir tmp #question about if such directory exists, maybe remove this line?
tmp="tmp.$RANDOM"
touch --date $date ./tmp/$tmp

find $1 -type f -not -newer ./tmp/$tmp ! -iname $tmp

rm -rf tmp