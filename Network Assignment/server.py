#!/bin/bash

import socket
import re
from string import digits
import string
from collections import defaultdict
import sys
import logging
import timeit


logging.basicConfig(filename="server.log",level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
songTrack= defaultdict(list)
global array
array=set()
fname="100worst.txt"
arrSong=[]
arrTitle=[]
arrArtist=[]


def digitRemover():
         remove_digits = str.maketrans('', '', digits)
         return remove_digits
def perfectLine(inputString):
     return bool(re.search(r'^\d.*\d$', inputString))

def seperatedTitleFirst(input):
        return bool(re.search(r'^\d.*\s$', input))
              
def seperatedTitleSecond(input):
        return bool(re.search(r'^\s\s+.*\d$', input))
def removeWhiteSpaces(string):
        return re.findall(r'.*.[\s|\w]*\w',string)
def splitSong(string):
        arrSong.append((re.split(r'\s\s+', string)))
def createDictionaryForPerfect():
        for i in arrSong:
                if len(i)==3:
                        songTrack[i[1]].append(i[0].translate(digitRemover()).replace("-","").strip())

                if len(i)==2:
                        arr=i[0].split('-')
                        songTrack[arr[2]]=arr[1]
                               
                
def createDictionaryForNonPerfect():
        for i in range(len(arrTitle)):
                song=arrArtist[i].strip().translate(digitRemover())
                editedSong=removeWhiteSpaces(song)
                songTrack[editedSong[0]].append(arrTitle[i].replace("-","").translate(digitRemover()).strip())

        
def checkMatching(dic,inputStr):
       regex= r'.*{}.*'.format(inputStr)
       for key in dic:
               if re.search(regex,key,re.IGNORECASE)!= None:
                       array.add("Artist: {} Song Title: {} " .format(key,str(songTrack.get((re.findall(regex,key,re.IGNORECASE)[0]),None))))
       if len(array)==0:
               return None
       else:
               return array               
def setSearch(f):
        with open(fname) as f:
                for line in f:
                        if seperatedTitleFirst(line)==True: 
                                if perfectLine(line)==True:
                                        splitSong(line)
                                else:
                                        arrTitle.append(line)

                        elif seperatedTitleSecond(line)==True:
                                        arrArtist.append(line)

        createDictionaryForPerfect()    
        createDictionaryForNonPerfect() 
def main():
    setSearch(fname)

    serverSocket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created for server")
    ip="127.0.0.1"
    port=3541
    try:
    # Connect to server and send data
        serverSocket.bind((ip,port))
        logging.info("Server is created ")
    except socket.error as e:
        print("Port is unavailable")
        print(e)
        logging.critical("Port is unavailable ")
        sys.exit()

    print("Server socket bound with ip {} port {}".format(ip,port))
    serverSocket.listen(1)
    logging.info("Listening to client... ")
    try:
        clientConnection, clientAddress = serverSocket.accept()
        print("Client Address: " + str(clientAddress)+"connected!")
        logging.info("Connection success! ")
        start = timeit.default_timer()

    except Exception as e:
        print("Client couldn't be connected")
        logging.critical("Client couldn't be connected ")
    clientConnection.send("Welcome".encode())
    clientConnection.send("Hi client".encode())
    while True:
        data=clientConnection.recv(1024).decode()
        print("[Client message] "+ str(data))
        clientConnection.send("Please enter artist name(Type Quit to quit): ".encode())
        while data!="Quit":
                data=clientConnection.recv(1024).decode()
                print("[Client message] "+ str(data))
                logging.info("Artist's name requested: {}".format(data))
                if data=="None":
                    clientConnection.send("Please put input. Type Quit to Exit ".encode())
                if data=="Quit":
                    clientConnection.send("Bye".encode())
                elif data!="None"and data!="Quit":
                    if checkMatching(songTrack,data)==None:
                        clientConnection.send("Nothing in the list. Type Quit to exit".encode())
                    if  checkMatching(songTrack,data)!=None:
                        string=""
                        for i in checkMatching(songTrack,data):
                                string=string+i+"\n"
                        string=string+"\n"+"Other artist? Type Quit to Exit"
                        clientConnection.send(string.encode())
                        array.clear()
        break 
    serverSocket.close()   
    stop = timeit.default_timer() 
    time=stop-start  
    logging.info("Time connected: {}".format(str(time)))        
 
main()
