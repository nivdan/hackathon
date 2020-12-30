#!/usr/bin/python3
from socket import *
import threading
import time
from _thread import *


def printit():
    # udp
    serverName = '192.168.175.166'
    serverPort = 13117
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = "0xfeedbeef"+"0x2"+"12000"
    threading.Timer(1.0, printit).start()
    clientSocket.sendto(message.encode("utf-8"), (serverName, serverPort))

def gameClientHandler(participantName):
    while gameFlag:
        try:
            participants[participantName].recv(1024)
            scores[participantName] += 1
        except:
            break
def threaded(connectionSocket):
    name = connectionSocket.recv(1024)
    if name.decode('utf-8') in participants:
        print("change your name")
    participants[name.decode('utf-8')] = connectionSocket
    # print(participants)

    # while True:
    # data received from client
    # data = c.recv(1024)
    # if not data:
    #   print('Bye')

    # lock released on exit
    #print_lock.release()

    # reverse the given string from client
    # data = data[::-1]

    # send back reversed string to client
    # c.send(data.upper())

    # connection closed
    # connectionSocket.close()
    
printit()
serverPortTcp = 12000
print("Server started, listening on IP address 172.1.0.4")
while 1:
    participants = {}
    scores = {}
    gameFlag = True
    #print_lock = threading.Lock()

    serverSocketTcp = socket(AF_INET, SOCK_STREAM)  # tcp
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
    for participantName in participants:
        if i % 2 == 0:
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
    '''
    while time.time() < timeout+timeout_start:
        for participantName in participants:  
            participants[participantName].setblocking(0)
            try:
                participants[participantName].recv(1024)
                scores[participantName] += 1
                print(scores[participantName])
            except:
                pass
    '''
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
    else:
        gameOverMsg += "Group 2 wins!\n\n"+"Congratulations to the winners:\n"+"==\n"
        for participantName in group2:
            gameOverMsg += participantName
    print(gameOverMsg)
    for participantName in participants:
        participants[participantName].close()

    print("Game over, sending out offer requests...")


# connectionSocket.close()
