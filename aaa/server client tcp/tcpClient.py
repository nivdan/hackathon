from socket import *
import threading
import sys, time, msvcrt

serverName = '192.168.175.166'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
while 1:
    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode("utf-8"))
    modifiedSentence = clientSocket.recv(1024)
    print ("From Server:", modifiedSentence.decode("utf-8"))
clientSocket.close()
