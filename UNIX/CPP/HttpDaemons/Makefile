CC=g++
CFLAGS=-o0 -Wall
LDFLAGS=
SOURCES+=src/task3/task3.cpp
SOURCES+=src/tools/tools.cpp
SOURCES+=src/task4/task4.cpp
SOURCES+=src/Main.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=daemon.out

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.c.o:
	$(CC) $(CFLAGS) $< -c -o $@