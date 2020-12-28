from socket import *
import threading
import time


def printit():
    # udp
    serverName = '192.168.175.166'
    serverPort = 13117
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = "0xfeedbeef"+"0x2"+"12000" 
    threading.Timer(5.0, printit).start()
    clientSocket.sendto(message.encode("utf-8"), (serverName, serverPort))

printit()