CC=g++
MPIC=mpic++
CFLAGS :=-std=c++11 -Wall
LDFLAGS=

TOOLSSOURCES=src/tools/TridiagonalSLE.cpp
TOOLSSOURCES+=src/tools/functions.cpp
TOOLSOBJECTS=$(TOOLSSOURCES:.cpp=.o)

ALGSOURCES=src/algorithm/MainAlg.cpp
ALGOBJECTS=$(ALGSOURCES:.cpp=.o)
ALGEXECUTABLE=app/alg.out

MPISOURCES=src/MPI/MainMPI.cpp
MPISOURCES+=src/MPI/MPIalg.cpp
MPISOURCES+=src/MPI/TridiagonalSLE.cpp
MPISOURCES+=src/MPI/functions.cpp
MPIOBJECTS=$(MPISOURCES:.cpp=.o)
MPIEXECUTABLE=app/MPIlab.out
$(OPENMPOBJECTS): CC := mpic++
MPIRUNNER=mpiexec

# define mpi_task =
# 	filename="data/MPItime.data"
# 	rm -f $filename
# 	touch $filename
# 	threadnum=8
# 	step=1
# 	. src/MPI/MPIparams.data
# 	echo "size: $size\nthreads_num	time(s)" >> $filename
# 	mpiexec -np 1 app/MPIlab.out
# 	for threadit in `seq 2 $step $threadnum`
# 	do
# 		mpiexec -np $threadit app/MPIlab.out
# 	done
# endef

OPENMPSOURCES=src/openmp/MainOpenMP.cpp
OPENMPSOURCES+=src/openmp/OpenMPalg.cpp
OPENMPOBJECTS=$(OPENMPSOURCES:.cpp=.o)
OPENMPEXECUTABLE=app/OpenMPlab.out
$(OPENMPOBJECTS): CFLAGS := $(CFLAGS) -fopenmp

PTHREADSOURCES=src/pthreads/MainPthreads.cpp
PTHREADSOURCES+=src/pthreads/PthreadsAlg.cpp
PTHREADOBJECTS=$(PTHREADSOURCES:.cpp=.o)
PTHREADEXECUTABLE=app/pthreadslab.out
$(PTHREADOBJECTS): CFLAGS := $(CFLAGS) -pthread

alg: $(ALGSOURCES) $(TOOLSSOURCES) $(ALGEXECUTABLE)

$(ALGEXECUTABLE): $(ALGOBJECTS) $(TOOLSOBJECTS)
	$(CC) $(LDFLAGS) $(ALGOBJECTS) $(TOOLSOBJECTS) -o $@

MPI: $(MPISOURCES) $(MPIEXECUTABLE)

$(MPIEXECUTABLE): $(MPIOBJECTS)
	$(MPIC) $(LDFLAGS) $(MPIOBJECTS) -o $@

# MPIrunCompare: ; $(value mpi_task)

# .PHONY: all test clean
# .ONESHELL:

MPIrunCompare:
	src/MPI/test.sh

MPIPyrunCompare:
	src/python/MPI/test.sh

MPIrun:
	$(MPIRUNNER) -np 3 $(MPIEXECUTABLE)

openmp: $(OPENMPSOURCES) $(TOOLSSOURCES) $(OPENMPEXECUTABLE)

$(OPENMPEXECUTABLE): $(OPENMPOBJECTS) $(TOOLSOBJECTS)
	$(CC) $(LDFLAGS) -fopenmp $(OPENMPOBJECTS) $(TOOLSOBJECTS) -o $@

pthreads: $(PTHREADSOURCES) $(TOOLSSOURCES) $(PTHREADEXECUTABLE)

$(PTHREADEXECUTABLE): $(PTHREADOBJECTS) $(TOOLSOBJECTS)
	$(CC) $(LDFLAGS) -pthread $(PTHREADOBJECTS) $(TOOLSOBJECTS) -o $@

check:
	python3 src/python/check.py

MPIpython:
	mpiexec -n 3 python3 src/python/MPI/main.py

.cpp.o:
	$(if $(findstring $<,$(MPISOURCES)),$(MPIC) $(CFLAGS) $< -c -o $@, $(CC) $(CFLAGS) $< -c -o $@)

clean:
	rm -rf $(ALGOBJECTS) $(ALGEXECUTABLE) $(MPIOBJECTS) $(MPIEXECUTABLE) $(OPENMPOBJECTS) $(OPENMPEXECUTABLE) $(PTHREADOBJECTS) $(PTHREADEXECUTABLE) $(TOOLSOBJECTS)