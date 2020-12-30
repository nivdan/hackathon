#!/usr/bin/python3
from socket import *
import threading
import sys
import time
import getch
from _thread import *
import select
import tty
import termios
from termcolor import colored

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
old_settings = termios.tcgetattr(sys.stdin)

clientName = "GoBackN1\n"
print('Client started, listening for offer requests...')

while 1:
    serverPort = 13119
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverSocket.bind(('', serverPort))
    message, clientAddress = serverSocket.recvfrom(2048)
    serverSocket.close()
    #print(message)
    #serverSocket.sendto(modifiedMessage, clientAddress)
    #serverPort = message[13::].decode('utf-8')
    message = message.hex()
    if (message[:8]!="feedbeef" or message[8:10]!= "02") :
        print(colored("message is corrupted",'red'))
        continue
    serverPort = int(message[10:],16)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    print(colored('Received offer from '+clientAddress[0]+' ,attempting to connect...','green'))

    try:
        clientSocket.connect((clientAddress[0], int(serverPort)))
        #clientSocket.connect((clientAddress[0],1111))
    except Exception as e:
        print(colored(str(e),'red'))
        continue
    clientSocket.send(clientName.encode('utf-8'))

    serverMsg = clientSocket.recv(1024)
    print(serverMsg.decode('utf-8'))
    #serverMsg = clientSocket.recv(1024)

    # while(len(serverMsg.decode('utf-8')) ==0):
    #  serverMsg = clientSocket.recv(1024)
    #print( serverMsg.decode('utf-8'))

    #while(len(serverMsg.decode('utf-8')) == 0):
    #    serverMsg = clientSocket.recv(1024)

    timeout = 10
    startTime = time.time()
    inp = None

    try:
        tty.setcbreak(sys.stdin.fileno())
        while 1:
            if isData():
                inp=sys.stdin.read(1)
                try:
                    clientSocket.send(inp.encode("utf-8"))
                except Exception as e:
                    print(e)
                    break
            if time.time() - startTime > timeout:
                break
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    print("Server disconnected, listening for offer requests...")
