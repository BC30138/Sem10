#!/bin/bash

filename="data/MPItime.data"
rm -f $filename
touch $filename
threadnum=8
step=1
. data/MPIparams.data
echo "size: $size\nthreads_num	time(s)" >> $filename
mpiexec -np 1 app/MPIlab.out
for threadit in `seq 2 $step $threadnum`
do
    mpiexec -np $threadit app/MPIlab.out
done