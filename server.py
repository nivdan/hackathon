#!/usr/bin/python3
from socket import *
import threading
import time
from _thread import *
import random

hostname = gethostname()
serverName = gethostbyname(hostname) 

def printit():
    # udp

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    message = bytes.fromhex("feedbeef")+bytes.fromhex("02")+bytes.fromhex("2EE0")
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
    name = connectionSocket.recv(1024)
    if name.decode('utf-8') in participants:
        print("change your name")
    participants[name.decode('utf-8')] = connectionSocket

printit()
serverPortTcp = 12000
print("Server started, listening on IP address "+serverName)
serverSocketTcp=None
while 1:
    participants = {}
    scores = {}
    gameFlag = True
    #print_lock = threading.Lock()
    
    serverSocketTcp = socket(AF_INET, SOCK_STREAM)  # tcp
    serverSocketTcp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocketTcp.settimeout(10)  # timeout for listening
    serverSocketTcp.bind(('', serverPortTcp))
    serverSocketTcp.listen(1)

    while 1:
        try:
            connectionSocket, addr = serverSocketTcp.accept()
            #print_lock.acquire()
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
        participantConnetSocket.send(
            startGameMsg.encode('utf-8'))

    for participantName in participants:
        scores[participantName] = 0
        start_new_thread(gameClientHandler, (participantName,))

    #timeout = 10
    #timeout_start = time.time()

    #while time.time() < timeout+timeout_start:
    #    pass
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

    print(gameOverMsg)
    for participantName in participants:
        participants[participantName].close()
    serverSocketTcp.shutdown(SHUT_RDWR)
    serverSocketTcp.close()
    print("Game over, sending out offer requests...")


# connectionSocket.close()
