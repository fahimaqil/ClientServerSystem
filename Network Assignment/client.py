#!/bin/bash


import socket
import sys
import time
import re
import logging
import timeit


logging.basicConfig(filename="client.log",level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
client_socket=socket.socket()

def utf8len(s):
    return len(s.encode('utf-8'))
try:
    client_socket.connect(("127.0.0.1",3541))
except  Exception:
    print("Something wrong")
print("Connected to localhost")
client_socket.settimeout(5.0)
try:
    data=client_socket.recv(1024).decode()
    
except Exception as e:
    print("Server is unavailable")
    print(e)
    logging.critical("Server is unavailable. Exited the program")
    sys.exit()
while True:
    try:
        data=client_socket.recv(1024).decode()
        print("[Message from server] " + str(data))
        res=client_socket.send("Hi Server".encode())
        data=client_socket.recv(1024).decode()
        print("[Message from server] " + str(data))
    except Exception as e:
        print("Sorry for your time.Something wrong with server!")
        print("Try to put any input to check")
        logging.critical("Something wrong with server")
    while data!="Bye":
        res=input("-->")
        start=timeit.default_timer()
        if res=="":
            client_socket.send("None".encode())
        else:
            try:
                client_socket.send(res.encode())
            except Exception as e:
                print("Error,Exiting the system....")
                logging.critical("Problem with server. Exited the program")
                break
        try:
            data=client_socket.recv(1024).decode()
            stop=timeit.default_timer()
            responseTime=stop-start
            logging.info("Server's response time: {}".format(str(responseTime)))
            logging.info("Length of bytes by server: {}".format(str(utf8len(data))))
        except Exception as e:
            print("Something wrong with the input u've given")
            print(e)
            logging.critical("Something wrong with the input u've given")

            client_socket.close()



        if data!="Bye":
            #data=client_socket.recv(1024).decode()
            print(data)
            
        if data=="Bye":
            #data=client_socket.recv(1024).decode()
            print(data)
            break
    break
client_socket.close()

