import socket
import sys
import Queue
import time
from thread import *
import threading

from threading import Thread

#Function for handling connections. This will be used to create threads
class clientThread(Thread):

    def __init__(self,socket,ip,port):
        Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = port
        print "Nueva thread iniciada"

    def run(self):

        # Sending message to connected client
        #self.socket.send('Bienvenido al chat, ingresa tu nombre')  # send only takes string
        self.socket.send(str(TIME_OUT))
        name = self.socket.recv(2048)
        identificador = self.socket.fileno()
        nickname = name + " " + str(identificador)
        nicknameMap.append(nickname)    
        
        #self.socket.send('Para enviar un mensaje a un usuario en especifico: send Usuario mensaje')
        # infinite loop so that function do not terminate and thread do not end.
        while True:
            #try:
            # Receiving from client
            self.socket.settimeout(TIME_OUT)
            orden = self.socket.recv(2048)
                
            if "Enviar " in orden:
                contenido = orden.partition(" ")                    
                contenidoUsr_Msg = contenido[2].partition(" ")                
                mensaje = name + ": " + contenidoUsr_Msg[2]                    

                receptor = contenidoUsr_Msg[0]
                print receptor
                estaConectado = 1 #no                    

                for recp in nicknameMap:                    
                    recepB = recp.partition(" ")
                    if recepB[0] == receptor:
                        recepID = int(recepB[2])                            

                        estaConectado = 0 #si
                        lock.acquire()
                        colaDeEnvio[recepID].put(mensaje)
                        lock.release()

                confEnvio = "Mensaje Enviado"

                self.socket.send(confEnvio)

            elif "Todos " in orden:
                ordenRec = orden.partition(" ")
                mensajeAll = ordenRec[2]                        
                msg = name + ": " + mensajeAll
                lock.acquire()
                for  q in colaDeEnvio.values():
                    q.put(msg)
                lock.release() 
            else:
                error = "Orden no valida"
                self.socket.send(error)    



class ClientThreaded(Thread):
    
    def __init__(self,sock):
        Thread.__init__(self)        
        self.sock = sock    
        print "Nueva thread para inciar el chat!"
               
    def run(self):         

         tcpsock2.listen(1)
         (conn2, addr) = tcpsock2.accept()
         welcomemsg = "hi"
         conn2.send(welcomemsg)
         chat = "initial"
         print "ind here is"
         print self.sock.fileno()
         while True:
             for p in nicknameMap:           #userfdmap contains mapping between usernames and their socket's file despcriptor which we use as index to access their respective queue
                 if str(self.sock.fileno()) in p:
                     connectionpresent = 1
                 else:
                     connectionpresent = 0         #We will use this to implement other features - no use as of now                                        
             try:
                 chat = colaDeEnvio[self.sock.fileno()].get(False)                
                 print chat
                 conn2.send(chat)     
             except Queue.Empty:                
                 chat = "none" 
                 time.sleep(2)
             except KeyError, e:
                 pass


lock = threading.Lock()  
global orden
orden = ""

colaDeEnvio = {}        
TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
TCP_PORT2 = 9999
BUFFER_SIZE = 20  # Normally 1024, but we want fast response
TIME_OUT = 1800.0 #seconds   - For time_out    Block_time is 60 seconds
BLOCK_TIME = 60.0

curusers = [] 
nicknameMap = []

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#host = socket.gethostname()
tcpsock.bind(('', TCP_PORT))

tcpsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock2.bind(('', TCP_PORT2))
         
threads = []
 
while True:
    tcpsock.listen(6)
    print "Esperando por conexiones de cliente.."
    (conn, (ip,port)) = tcpsock.accept()
    q = Queue.Queue()
    lock.acquire()
   
   
    colaDeEnvio[conn.fileno()] = q
    lock.release()
    
           
    print "Nuevo thread with " , conn.fileno()
    newthread = clientThread(conn,ip,port)
    newthread.daemon = True
    newthread.start()
    newthread2 = ClientThreaded(conn)
    newthread2.daemon = True

    newthread2.start()
    threads.append(newthread)
    threads.append(newthread2)
        
for t in threads:
    t.join()
    
    print "eND"
