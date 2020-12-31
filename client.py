#!/usr/bin/python3
from socket import *
import threading
import sys
import time
from _thread import *
import select
import tty
import termios
from termcolor import colored
# constants


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


serverPortUdp = 13117
recvBufferSize1024 = 1024
recvBufferSize2048 = 2048
timeOutConstant = 10
# function that check if any key is pressed


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


old_settings = termios.tcgetattr(sys.stdin)

clientName = "GoBackN\n"
print(f"{bcolors.OKBLUE}Client started, listening for offer requests... {bcolors.ENDC}")

# Main loop
while 1:
    # Trying to receive server to connect to
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    serverSocket.bind(('', serverPortUdp))
    message, clientAddress = serverSocket.recvfrom(recvBufferSize2048)
    serverSocket.close()
    # got message, clossing the socket and checking that the message is not corrupted
    message = message.hex()
    if (message[:8] != "feedbeef" or message[8:10] != "02"):
        print(f"{bcolors.FAIL}message is corrupted{bcolors.ENDC}")
        continue
    serverPortTcp = int(message[10:], 16)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    print(f"{bcolors.OKGREEN}Received offer from " +
          clientAddress[0]+", attempting to connect..."+f"{bcolors.ENDC}")
    try:
        # Trying to create tcp connection with the server
        clientSocket.connect((clientAddress[0], int(serverPortTcp)))
    except Exception as e:
        # Throw exection if the server refuse the connection
        print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
        continue
    try:
        # Trying to send the nick name to the server after the tcp connection established
        clientSocket.send(clientName.encode('utf-8'))
        serverMsg = clientSocket.recv(recvBufferSize1024)
    except Exception as e:
        print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
        continue
    # Client recieve the start message
    print(f"{bcolors.OKCYAN}"+serverMsg.decode('utf-8')+f"{bcolors.ENDC}")
    startTime = time.time()
    inp = None
    # Loop to get keys from the client
    try:
        tty.setcbreak(sys.stdin.fileno())
        while 1:
            if isData():
                inp = sys.stdin.read(1)
                try:
                    clientSocket.send(inp.encode("utf-8"))
                except Exception as e:
                    print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
                    break
            if time.time() - startTime > timeOutConstant:
                break
            time.sleep(0.01)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    try:
        gameOverMsg = clientSocket.recv(recvBufferSize1024)
    except Exception as e:
        print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
        continue
    # print the end message
    print(f"{bcolors.WARNING}"+gameOverMsg.decode('utf-8')+f"{bcolors.ENDC}")
    print("Server disconnected, listening for offer requests...")
