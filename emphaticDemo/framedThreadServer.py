#! /usr/bin/env python3
import sys, os, socket, params, time
from threading import Thread, Lock
from framedSock import FramedStreamSock

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        Thread.__init__(self, daemon=True)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
       
    def run(self):
        while True:
            X= True
            msg =''
            while X:
                if msg is not None:
                    msg += self.fsock.receivemsg().decode()+" "
                print("Printing Message !!!!!!!!!!!! =",msg)
                if not msg:
                    if self.debug: print(self.fsock, "server thread done")
                    return
                if("//FINISH!" in msg):
                    X = False

               # msg =msg.decode()
                #msg+=" "

            #mutex.acquire()                                                     #wait for this process finish
            NewFile = msg.replace("\x00", "\n") #go back to normal
            Separated = NewFile.split("//NAME//")
            try:                                                                #if File exist then need to change the name
                l = open(Separated[0], "r")
                l.close()
                mutex.acquire()
                print("HERE!!!!!!!",Separated)
                ChangeName = Separated[0].split(".")
                RC = str(ServerThread.requestCount)
                NewName = ChangeName[0]+"("+RC+")"+"."+ChangeName[1]

                doc = open(NewName, "w")
                doc.write(Separated[1])
                doc.close()

                mutex.release()

                requestNum = ServerThread.requestCount
                time.sleep(0.001)
                ServerThread.requestCount = requestNum + 1
                msg = ("%s! (%d)" % (msg, requestNum)).encode()
                self.fsock.sendmsg(msg)

            except FileNotFoundError:                                           #does not exist the file so I can leave the name

                doc = open(Separated[0], "w")
                doc.write(Separated[1])
                doc.close()

                #mutex.release()

                requestNum = ServerThread.requestCount
                time.sleep(0.001)
                ServerThread.requestCount = requestNum + 1
                msg = ("%s! (%d)" % (msg, requestNum)).encode()
                self.fsock.sendmsg(msg)



mutex = Lock()
while True:
    sock, addr = lsock.accept()
    ServerThread(sock, debug)
