#!/usr/bin/env python
import sys
import socket
import time
import threading
from threading import Thread
from SocketServer import ThreadingMixIn

class ServerThread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
     #   print "New thread started for write"

    def run(self):
        print "Conectado!" 
        
        while True:
            starttime = time.time() 
            print "Bienvenido:\nPara enviar un mensaje a todos escribe:\nPara uno especifico Enviar Usuario Mensaje"           
            orden = raw_input(" Ingrese orden: ")                            
            self.socket.send(orden)                        

class ServerThreadread(Thread):
 
    def __init__(self,socket):
        Thread.__init__(self)
        self.socket = socket
        
      #  print "New thread started for chat display"
  
    def run(self):
        
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2.connect((TCP_IP, TCP_PORT2))
        welcomemsg = s2.recv(BUFFER_SIZE)
        chat = "initial"
        print welcomemsg
        
        while True:
            if log == 0:
              #  print "inside loop"
                chat=s2.recv(BUFFER_SIZE)
                print chat
                time.sleep(5)
                
            if log == 1:
              #  print "going to exit"
                s2.close()
                sys.exit() 

        
TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
TCP_PORT2 = 9999
BUFFER_SIZE = 1024

threads = []
global log
log = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
TIME_OUT = s.recv(BUFFER_SIZE)   #Server exchanges tmeout details with client at the start of every socket

username = raw_input('Bienvenido al chat, ingresa tu nombre: ')
s.send(username)
#s.send(nombre)
try:
    newthread = ServerThread(s)
    newthread.daemon = True
    newthread2 = ServerThreadread(s)
    newthread2.daemon = True
    newthread.start()
    newthread2.start()
    threads.append(newthread)
    threads.append(newthread2)
    while True:
        for t in threads:
            t.join(600)
            if not t.isAlive():
                break
        break        
                    
except KeyboardInterrupt:    
    sys.exit()
