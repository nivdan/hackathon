from socket import *
import threading
import sys
import time
import msvcrt

serverPort = 13117
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
serverSocket.bind(('', serverPort))
print('Client started, listening for offer requests...')
# while 1:
message, clientAddress = serverSocket.recvfrom(2048)
print(message.decode('utf-8'))
