from socket import *
import threading
import time
from _thread import *

print_lock = threading.Lock() 

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print ('The server is ready to receive')
def threaded(c): 
    while True: 
  
        # data received from client 
        data = c.recv(1024) 
        if not data: 
            print('Bye') 
              
            # lock released on exit 
            print_lock.release() 
            break
  
        # reverse the given string from client 
        data = data[::-1] 
  
        # send back reversed string to client 
        c.send(data.upper()) 
  
    # connection closed 
    c.close() 
while 1:
     connectionSocket, addr = serverSocket.accept()
     start_new_thread(threaded, (connectionSocket,))
     #sentence = connectionSocket.recv(1024)
     #capitalizedSentence = sentence.upper()
     #connectionSocket.send(capitalizedSentence)
#connectionSocket.close()
