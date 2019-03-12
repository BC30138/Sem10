#!/bin/bash

IFS='/' read -ra datearray <<< "$2" 

date=${datearray[2]}"-"${datearray[1]}"-"${datearray[0]}

touch --date $date tmp

find $1 -type f -not -newer tmp | grep -v $1"tmp"

rm -rf tmp