#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

IFS='/' read -ra datearray <<< "$2" 

date=${datearray[2]}"-"${datearray[1]}"-"${datearray[0]}

touch --date $date tmp

find $1 -type f -not -newer tmp ! -iname "tmp" 

rm -rf tmp