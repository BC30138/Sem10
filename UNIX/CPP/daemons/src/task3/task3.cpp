#include <stdio.h>
#include <stdlib.h> // некоторые важные переменные, такие EXIT_SUCCESS и переменные, вроде size_t
#include <unistd.h> // POSIX стандартные типы
#include <sys/stat.h> // для того, чтобы варнинга не было о том, что не стоит
                      // использовать umask заданный неявно
#include <syslog.h> // для работы с журналом
#include <signal.h> // для работы с сигналами
#include <dirent.h> // для работы с файловой системой
#include "../tools/tools.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <iostream>
#include <fstream>

using namespace std;

int listener;
string answerHeadHTML = "HTTP/1.1 200 OK\r\nVersion: HTTP/1.1\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: ";
string answerHeadPicture = "HTTP/1.1 200 OK\r\nVersion: HTTP/1.1\r\nContent-Type: image/png\r\nContent-Length: ";

void signal_handler_task_3(int sig) {
    switch (sig)
    {
    case SIGTERM:
        syslog(LOG_DAEMON, "daemon terminated");
        close(listener);
        closelog();
        exit(0);
        break;
    }
}

void getData(string& tmpStr)
{
    tmpStr.erase(tmpStr.begin(), tmpStr.begin() + 4);
    int count = 0;
    while(tmpStr.at(count) !='\r')
        count++;
    tmpStr.erase(tmpStr.begin() + count, tmpStr.end());
    tmpStr.erase(tmpStr.end() - 9, tmpStr.end());
}

void run_task_3() {
    daemonize_();
    openlog("task3daemon", 0, LOG_USER);
    syslog(LOG_DAEMON, "daemon has been started");
    signal(SIGTERM, signal_handler_task_3);

    int sock;
    struct sockaddr_in addr;
    char buff[1024];// messages
    listener = socket(AF_INET, SOCK_STREAM, 0);

    if(listener < 0){
        syslog(LOG_DAEMON, "Error while creating socket.");
        exit(1);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(8484);
    addr.sin_addr.s_addr = INADDR_ANY;

    if(bind(listener, (struct sockaddr *)&addr, sizeof(addr)) < 0){
        syslog(LOG_DAEMON, "Socket is already used.");
        exit(2);
    }

    listen(listener, 1);
    while(1){
        sock = accept(listener, NULL, NULL);
        if(sock < 0){
            syslog(LOG_DAEMON, "Socket can not be accepted.");
            exit(3);
        }
        switch(fork()){
            case -1:
                syslog(LOG_DAEMON, "!!!Fork!!! can not be created.");
                break;
            case 0:
            {
                close(listener);
                if(recv(sock, buff , 1024, 0) < 0)
                    syslog(LOG_DAEMON, "Data hasn't been recieved.");

                string recieveData = buff;//Полученный GET запрос
                string body;//Тело http ответа
                string answer;//http ответ

                getData(recieveData);//Путь запрашиваемого файла
                if(recieveData.find(".html") != std::string::npos)//Запрос странички
                    answer = answerHeadHTML;
                else if(recieveData.find(".png") != std::string::npos)//Запрос картинки
                    answer = answerHeadPicture;



                std::ifstream webpage(recieveData, ios::binary);
                //Копируем содержимое файла
                string text((
                                std::istreambuf_iterator<char>(webpage)),
                            (std::istreambuf_iterator<char>()));

                body = text;
                answer+=to_string(body.size());
                answer+="\r\n\r\n";
                answer+=body;

                if(send(sock, answer.data(),answer.size(), 0) < 0)
                    syslog(LOG_DAEMON, "Data hasn't been sent.");

                close(sock);
                exit(0);
            }
            default:
                close(sock);
        }
    }
}