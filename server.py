#!/usr/bin/python3
from socket import *
import threading
import time
from _thread import *
import random

hostname = gethostname()
serverName = gethostbyname(hostname) 
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
def printit():
    # udp
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    message = bytes.fromhex("feedbeef")+bytes.fromhex("02")+bytes.fromhex("0855")
    threading.Timer(1.0, printit).start()
    serverPort = 13119
    clientSocket.sendto(message, ('<broadcast>', serverPort))

def gameClientHandler(participantName):
    while gameFlag:
        try:
            char=participants[participantName].recv(1024)
            if char.decode('utf-8')=='':
                break
            scores[participantName] += 1
        except:
            break
def threaded(connectionSocket):
    try:
        name = connectionSocket.recv(1024)
        if name.decode('utf-8') in participants:
            print(f"{bcolors.FAIL}change your name{bcolors.ENDC}")
        participants[name.decode('utf-8')] = connectionSocket
    except Exception as e:
        print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")

printit()
serverPortTcp = 2133
print(f"{bcolors.OKBLUE}Server started, listening on IP address "+serverName+f"{bcolors.ENDC}")
serverSocketTcp=None
while 1:
    participants = {}
    scores = {}
    gameFlag = True
    serverSocketTcp = socket(AF_INET, SOCK_STREAM)  # tcp
    serverSocketTcp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocketTcp.settimeout(10)  # timeout for listening
    serverSocketTcp.bind(('', serverPortTcp))
    serverSocketTcp.listen(1)

    while 1:
        try:
            connectionSocket, addr = serverSocketTcp.accept()
            start_new_thread(threaded, (connectionSocket,))
        except:
            break
    # print('timeout')
    group1 = []
    group2 = []
    i = 0

    participantsKeyList=list(participants.keys())
    random.shuffle(participantsKeyList)

    for participantName in participants:
        if participantsKeyList.index(participantName)<(len(participantsKeyList)/2):
            group1.append(participantName)
        else:
            group2.append(participantName)
        i += 1

    startGameMsg = "Welcome to Keyboard Spamming Battle Royale.\n"
    startGameMsg += "Group 1:\n==\n"
    for participantName in group1:
        startGameMsg += participantName
    startGameMsg += "Group 2:\n==\n"
    for participantName in group2:
        startGameMsg += participantName

    startGameMsg += 'Start pressing keys on your keyboard as fast as you can!!'

    for participantConnetSocket in participants.values():
        try:
            participantConnetSocket.send(
                startGameMsg.encode('utf-8'))
        except Exception as e:
            print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")

    for participantName in participants:
        scores[participantName] = 0
        start_new_thread(gameClientHandler, (participantName,))

    time.sleep(10)
    gameFlag = False

    group1Score = 0
    group2Score = 0
    for participantName in participants:
        if participantName in group1:
            group1Score += scores[participantName]
        else:
            group2Score += scores[participantName]

    gameOverMsg = "Game over!\n"+"Group 1 typed in " + \
        str(group1Score) + " characters. Group 2 typed in " + \
        str(group2Score)+" characters.\n"
    if group1Score > group2Score:
        gameOverMsg += "Group 1 wins!\n\n"+"Congratulations to the winners:\n"+"==\n"
        for participantName in group1:
            gameOverMsg += participantName
    elif group1Score < group2Score:
        gameOverMsg += "Group 2 wins!\n\n"+"Congratulations to the winners:\n"+"==\n"
        for participantName in group2:
            gameOverMsg += participantName
    else:
        gameOverMsg += "Its a tie!\n\n"+"There are no winners in this game!\n"

    #print(gameOverMsg)
    for participantName in participants:
        try:
            participants[participantName].send(gameOverMsg.encode('utf-8'))
            participants[participantName].shutdown(SHUT_RDWR)
            participants[participantName].close()
        except Exception as e :
            print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
    serverSocketTcp.shutdown(SHUT_RDWR)
    serverSocketTcp.close()
    print(f"{bcolors.WARNING}Game over, sending out offer requests...{bcolors.ENDC}")


# connectionSocket.close()
