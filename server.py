#!/usr/bin/python3
from socket import *
import threading
import time
from _thread import *
import random

hostname = gethostname()
serverName = gethostbyname(hostname)
#constants
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
#new comment
offerCode ="02"
serverPortTcp = 2133
serverPortTcpHex = "0855"
recvBufferSize=1024
timeOutConstant=10
serverPortUdp=13117

# Thread that send the broadcast message in the udp chanel every second.
def printit():
    # udp
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    message = bytes.fromhex("feedbeef") + \
        bytes.fromhex(offerCode)+bytes.fromhex(serverPortTcpHex)
    threading.Timer(1.0, printit).start()
    clientSocket.sendto(message, ('<broadcast>', serverPortUdp))
# Thread that handle the messages from the client (thread per client)


def gameClientHandler(participantName):
    while gameFlag:
        try:
            char = participants[participantName].recv(recvBufferSize)
            if char.decode('utf-8') == '':
                break
            scores[participantName] += 1
        except:
            break
# Thread that get the nick name from the client (thread per client)


def threaded(connectionSocket):
    try:
        name = connectionSocket.recv(recvBufferSize)
        if name.decode('utf-8') in participants:
            print(f"{bcolors.FAIL}change your name{bcolors.ENDC}")
        participants[name.decode('utf-8')] = connectionSocket
    except Exception as e:
        print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")


# start to send udp broadcast messages
printit()

print(f"{bcolors.OKBLUE}Server started, listening on IP address " +
      serverName+f"{bcolors.ENDC}")
serverSocketTcp = None
# Server main Loop
while 1:
    # reset the dictionaries
    participants = {}
    scores = {}
    gameFlag = True
    # Open socket to recieve connections for 10 seconds
    serverSocketTcp = socket(AF_INET, SOCK_STREAM)  # tcp
    serverSocketTcp.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocketTcp.settimeout(timeOutConstant)  # timeout for listening
    serverSocketTcp.bind(('', serverPortTcp))
    serverSocketTcp.listen(1)
    # Loop that accepting the tcp connects
    while 1:
        try:
            connectionSocket, addr = serverSocketTcp.accept()
            start_new_thread(threaded, (connectionSocket,))
        except:
            break
    # 10 seconds have passed now we divide the participants into to random groups
    group1 = []
    group2 = []
    participantsKeyList = list(participants.keys())
    random.shuffle(participantsKeyList)
    for participantName in participants:
        if participantsKeyList.index(participantName) < (len(participantsKeyList)/2):
            group1.append(participantName)
        else:
            group2.append(participantName)

    startGameMsg = "Welcome to Keyboard Spamming Battle Royale.\n"
    startGameMsg += "Group 1:\n==\n"
    for participantName in group1:
        startGameMsg += participantName
    startGameMsg += "Group 2:\n==\n"
    for participantName in group2:
        startGameMsg += participantName

    startGameMsg += 'Start pressing keys on your keyboard as fast as you can!!'
    # Sending welcome message to all the participands
    for participantConnetSocket in participants.values():
        try:
            participantConnetSocket.send(
                startGameMsg.encode('utf-8'))
        except Exception as e:
            print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
    # stating thread to handle each of the participands
    for participantName in participants:
        scores[participantName] = 0
        start_new_thread(gameClientHandler, (participantName,))
    # waiting until the game ends
    time.sleep(timeOutConstant)
    gameFlag = False
    # calculating each group score
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
    # sending game over message to all the participants
    # print(gameOverMsg)
    for participantName in participants:
        try:
            participants[participantName].send(gameOverMsg.encode('utf-8'))
            participants[participantName].shutdown(SHUT_RDWR)
            participants[participantName].close()
        except Exception as e:
            print(f"{bcolors.FAIL}"+str(e)+f"{bcolors.ENDC}")
    serverSocketTcp.shutdown(SHUT_RDWR)
    serverSocketTcp.close()
    # Going back to offer request to clients
    print(f"{bcolors.WARNING}Game over, sending out offer requests...{bcolors.ENDC}")
