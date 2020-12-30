#!/usr/bin/python3
from socket import *
import threading
import sys, time, msvcrt
from _thread import *

clientName = "aaa\n"
print('Client started, listening for offer requests...')

while 1:
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverSocket.bind(('', serverPort))
    # while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    #print(message.decode('utf-8'))
    serverSocket.close()

    #serverSocket.sendto(modifiedMessage, clientAddress)
    serverPort = message[13::].decode('utf-8')
    #print(serverPort)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print('Received offer from 172.1.0.4,attempting to connect...')
    #print(clientAddress)


    #sentence = input('Input lowercase sentence:')

    clientSocket.connect((clientAddress[0], int(serverPort)))
    clientSocket.send(clientName.encode('utf-8'))

    serverMsg = clientSocket.recv(1024)
    print( serverMsg.decode('utf-8'))
    #serverMsg = clientSocket.recv(1024)

    # while(len(serverMsg.decode('utf-8')) ==0):
    #  serverMsg = clientSocket.recv(1024)
    #print( serverMsg.decode('utf-8'))

    while(len(serverMsg.decode('utf-8')) == 0):
        serverMsg = clientSocket.recv(1024)


    timeout = 10
    startTime = time.time()
    inp = None

    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            clientSocket.send(inp)
        elif time.time() - startTime > timeout:
            break

    #if inp:
    #    print "Config selected..."
    #else:
    #    print ("Timed out...")
    #print('timeout')
    #time.sleep(3)
    #clientSocket.send('test'.encode('utf-8'))

    #serverMsg = clientSocket.recv(1024)
    #print(serverMsg.decode('utf-8'))
    
    print("Server disconnected, listening for offer requests...")

