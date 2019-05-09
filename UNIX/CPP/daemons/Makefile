CC=gcc
CFLAGS=-o0 -Wall
LDFLAGS=
SOURCES=src/example/example.c
SOURCES+=src/task2/task2.c
SOURCES+=src/task3/task3.c
SOURCES+=src/tools/tools.c
SOURCES+=src/Main.c
OBJECTS=$(SOURCES:.c=.o)
EXECUTABLE=daemon.out

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@