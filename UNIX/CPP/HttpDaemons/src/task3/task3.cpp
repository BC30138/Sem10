
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно
#include <syslog.h> // для работы с журналом
#include <signal.h> // для работы с сигналами
#include <dirent.h> // для работы с файловой системой
#include <string.h>
#include "../tools/tools.h"
#include <sys/socket.h>
#include <netinet/in.h>



using namespace std;

string answerHeadHTML = "HTTP/1.1 200 OK\r\nVersion: HTTP/1.1\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: ";
string answerHeadPicture = "HTTP/1.1 200 OK\r\nVersion: HTTP/1.1\r\nContent-Type: image/png\r\nContent-Length: ";
string answerNotFound = "HTTP/1.1 404 Not Found\r\nConnection: close\r\nVersion: HTTP/1.1\r\nContent-type: text/html\r\nContent-length: ";

int listener;

void signal_handler_task_3(int sig) {
    switch (sig)
    {
    case SIGTERM:
        syslog(LOG_WARNING, "Daemon terminated!");
        close(listener);
        closelog();
        exit(0);
        break;
    }
}

void getData(string& tmpStr)
{
    tmpStr.erase(tmpStr.begin(), tmpStr.begin() + 5);
    int count = 0;
    while(tmpStr.at(count) !='\r')
        count++;
    tmpStr.erase(tmpStr.begin() + count, tmpStr.end());
    tmpStr.erase(tmpStr.end() - 9, tmpStr.end());
}

void run_task_3() {
    char path[1024];
    getcwd(path, sizeof(path));
    strcat(path, "/data");

    daemonize_(path);
    openlog("task3daemon", 0, LOG_DAEMON);
    syslog(LOG_WARNING, "daemon has been started");
    signal(SIGTERM, signal_handler_task_3);

    int sock;
    struct sockaddr_in addr;
    char buff[1024];// messages
    listener = socket(AF_INET, SOCK_STREAM, 0);

    if(listener < 0){
        syslog(LOG_WARNING, "Error while creating socket.");
        exit(1);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(8485);
    addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(listener, (struct sockaddr *)&addr, sizeof(addr)) < 0){
        syslog(LOG_WARNING, "Socket is already used.");
        exit(2);
    }

    listen(listener, 1);
    while(1){
        sock = accept(listener, NULL, NULL);
        if(sock < 0){
            syslog(LOG_WARNING, "Socket can not be accepted.");
            exit(3);
        }
        switch(fork()){
            case -1:
                syslog(LOG_WARNING, "Fork can not be created.");
                break;
            case 0:
            {
                close(listener);
                if(recv(sock, buff , 1024, 0) < 0)
                    syslog(LOG_WARNING, "Data hasn't been recieved.");

                string recieveData = buff;//Полученный GET запрос
                string body;//Тело http ответа
                string answer;//http ответ

                getData(recieveData);//Путь запрашиваемого файла

                if(recieveData.find(".html") != std::string::npos)//Запрос странички
                    answer = answerHeadHTML;
                else if(recieveData.find(".png") != std::string::npos)//Запрос картинки
                    answer = answerHeadPicture;


                std::ifstream webpage(recieveData);
                if (webpage.fail()){
                    answer = answerNotFound;
                    body = "<HTML><HEAD><TITLE>404 - Not Found</TITLE></HEAD><BODY BGCOLOR=\"FFFFFF\"><H1>404 - Not Found</H1><HR></BODY></HTML>";
                }
                else {
                    string text((
                                istreambuf_iterator<char>(webpage)),
                            (istreambuf_iterator<char>()));

                    body = text;
                }
                answer+=to_string(body.size());
                answer+="\r\n\r\n";
                answer+=body;
                if(send(sock, answer.c_str() ,answer.size(), 0) < 0)
                    syslog(LOG_WARNING, "Data hasn't been sent.");
                close(sock);
                exit(0);
            }
            default:
                close(sock);
        }
    }
}