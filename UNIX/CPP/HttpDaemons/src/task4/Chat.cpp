#include<iostream>
#include<sys/types.h>
#include<sys/stat.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<stdio.h>
#include<unistd.h>
#include<fcntl.h>
#include<set>
#include <algorithm>
#include<syslog.h>
#include<signal.h>

#include "../tools/tools.h"

using namespace std;

#define port 8087

int listener;
void signal_handler_server(int SIG) {
    switch (SIG)
    {
    case SIGTERM:
        syslog(LOG_WARNING, "Daemon has been terminated.");
        close(listener);
        closelog();
        exit(0);
    default:
        break;
    }
}

void launch_server() {
    char path[1024];
    getcwd(path, sizeof(path));
    strcat(path, "/data");
    daemonize_(path);

    openlog("ChatServer", 0, LOG_WARNING);

    signal(SIGTERM, signal_handler_server);

    syslog(LOG_WARNING, "daemon has been started.");

    struct sockaddr_in addr;
    char buf[1024];
    int bytesRead;

    listener = socket(AF_INET, SOCK_STREAM, 0);
    if(listener < 0){
        syslog(LOG_WARNING, "Socket can't be created.");
        exit(1);
    }

    fcntl(listener, F_SETFL, O_NONBLOCK);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    if(bind(listener, (struct sockaddr*)&addr, sizeof(addr)) < 0){
        syslog(LOG_DAEMON, "Socket is already used.");
        exit(2);
    }

    listen(listener, 2);
    set<int> clients;

    while(1){
        //Заполняем множество сокетов
        fd_set readset;
        FD_ZERO(&readset);
        FD_SET(listener, &readset);

        for(set<int>:: iterator it = clients.begin(); it != clients.end(); it++)
            FD_SET(*it, &readset);
        //Задаем таймаут
        timeval timeout;
        timeout.tv_sec = 15;
        timeout.tv_usec = 0;

        //Ждем событие в одном из сокетов
        int mx = max(listener, *max_element(clients.begin(), clients.end()));
        if(select(mx+1, &readset, NULL, NULL, &timeout) < 0){
            syslog(LOG_DAEMON, "Select problem.");
            exit(3);
        }

        //Определяем тип события и выполняем соответствующие действия.
        if(FD_ISSET(listener, &readset)){
            //Поступил новый запрос на соединение, используем accept
            int sock = accept(listener, NULL, NULL);
            if(sock < 0){
                syslog(LOG_DAEMON, "Accept error.");
                exit(3);
            }
            fcntl(sock, F_SETFL, O_NONBLOCK);
            clients.insert(sock);
        }
        for(set<int>::iterator it = clients.begin(); it != clients.end(); it++){
            if(FD_ISSET(*it, &readset)){
                //Поступили данные от клиента, читаем их
                bytesRead = recv(*it, buf, 1024, 0);
                if(bytesRead <= 0){
                    //Соединения разорвано удаляем сокет из множества
                    close(*it);
                    clients.erase(*it);
                    continue;
                }
                //Отправляем данные
                for(set<int>::iterator member = clients.begin(); member != clients.end(); member++){
                    if(member != it)
                        send(*member, buf, bytesRead, 0);
                }
            }
        }
    }
}

string username;
int client_sock;
void *read (void *dummyPt)
{
    while(true){

        char buf[1024] = {'\0'};
        recv(client_sock, buf, sizeof(buf) + username.size(), 0);
        string recieveData = buf;
        // string line = "\033[31m";

        // int i=0;
        // for(int i = 0; i < recieveData.size(); ++i) {

            //ВНИМАНИЕ ВОПРОС - Я ДЕЙСТВИТЕЛЬНО НЕ ПОНИМАЮ И НЕ МОГУ НАЙТИ ПОЧЕМУ ОН НЕ ПЕЧАТАЕТ НИЧЕГО КРОМЕ НИЖЕ ПРЕДСТАВЛЕНОГО,
            //А Я ВЕДЬ ХОЧУ ЕЩЕ И ИМЯ КЛИЕНТА НАПИСАТЬ, А ТАКЖЕ СОВЕРШЕННО НЕ ЯСНО ПОЧЕМУ ВПЕРВЫЕ ИМЯ ПОЛЬЗОВАТЕЛЯ ДУБЛИРУЕТСЯ
        if (recieveData.size() != 0) {
            cout << "\n" << recieveData;
        }
            // line+=recieveData.at(i);
        // }
        // line+="\033[0m";
        // for(;recieveData.at(i) != '\n'; ++i) line+=recieveData.at(i);
        // line+=username;
        // cout << line;
    }
}

int launch_client() {
    pthread_t threads[1];
    pthread_create(&threads[0], NULL, read, NULL);
    pthread_detach(threads[0]);

    struct sockaddr_in addr;
    client_sock = socket(AF_INET, SOCK_STREAM, 0);
    if(client_sock < 0){
        perror("Socket can't be created");
        exit(1);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    if(connect(client_sock, (struct sockaddr*)&addr, sizeof(addr)) < 0){
        perror("Socket can't be connected");
        exit(2);
    }

    cout << "\033[1;36mEnter username: \033[0m";
    cin >> username;

    while(1){
        string mess;
        cout << "\033[1;32m" << username << "#\033[0m";
        getline(cin, mess);
        mess+="\n";

        if(mess == string(":exit\n")){//Выход из чата
            close(client_sock);
            return 0;
        }
        else{
            string result = username;
            result+="# ";
            result+=mess;
            mess = result;
            send(client_sock, mess.data(), mess.size(), 0);
        }
    }
    close(client_sock);

    return 0;
}