CC=g++
CFLAGS=-o0 -Wall
LDFLAGS=
TASK3SOURCES+=src/task3/task3.cpp
TASK3SOURCES+=src/task3/Main.cpp
TASK3SOURCES+=src/tools/tools.cpp
TASK3OBJECTS=$(TASK3SOURCES:.cpp=.o)
TASK3EXECUTABLE=task3.out

SERVERSOURCES+=src/task4/Chat.cpp
SERVERSOURCES+=src/tools/tools.cpp
SERVERSOURCES+=src/task4/ChatServer.cpp
SERVEROBJECTS=$(SERVERSOURCES:.cpp=.o)
SERVEREXECUTABLE=ChatServer.out

CLIENTSOURCES+=src/task4/Chat.cpp
CLIENTSOURCES+=src/tools/tools.cpp
CLIENTSOURCES+=src/task4/ChatClient.cpp
CLIENTOBJECTS=$(CLIENTSOURCES:.cpp=.o)
CLIENTEXECUTABLE=ChatClient.out

task3: $(TASK3SOURCES) $(TASK3EXECUTABLE)

$(TASK3EXECUTABLE): $(TASK3OBJECTS)
	$(CC) $(LDFLAGS) $(TASK3OBJECTS) -o $@

server: $(SERVERSOURCES) $(SERVEREXECUTABLE)

$(SERVEREXECUTABLE): $(SERVEROBJECTS)
	$(CC) $(LDFLAGS) $(SERVEROBJECTS) -o $@

client: $(CLIENTSOURCES) $(CLIENTEXECUTABLE)

$(CLIENTEXECUTABLE): $(CLIENTOBJECTS)
	$(CC) $(LDFLAGS) $(CLIENTOBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -c -o $@

clean:
	rm -rf $(TASK3OBJECTS) $(TASK3EXECUTABLE) $(SERVEROBJECTS) $(SERVEREXECUTABLE) $(CLIENTOBJECTS) $(CLIENTEXECUTABLE)