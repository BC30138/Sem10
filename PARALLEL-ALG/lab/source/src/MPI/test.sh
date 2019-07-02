#!/bin/bash

filename="data/MPItime.data"
rm -f $filename
touch $filename
start=1
step=1
threadnum=24
. data/MPIparams.data
echo "size: $size\nthreads_num	time(s)" >> $filename
for threadit in `seq $start $step $threadnum`
do
    mpiexec -np $threadit app/MPIlab.out
done