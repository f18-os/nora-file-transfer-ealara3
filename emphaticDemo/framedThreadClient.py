#! /usr/bin/env python3

# Echo client program
import socket, sys, re
import params
from framedSock import FramedStreamSock
from threading import Thread
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "localhost:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

class ClientThread(Thread):
    def __init__(self, serverHost, serverPort, debug):
        Thread.__init__(self, daemon=False)
        self.serverHost, self.serverPort, self.debug = serverHost, serverPort, debug
        self.start()
    def run(self):
       s = None
       for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
           af, socktype, proto, canonname, sa = res
           try:
               print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
               s = socket.socket(af, socktype, proto)
           except socket.error as msg:
               print(" error: %s" % msg)
               s = None
               continue
           try:
               print(" attempting to connect to %s" % repr(sa))
               s.connect(sa)
           except socket.error as msg:
               print(" error: %s" % msg)
               s.close()
               s = None
               continue
           break

       if s is None:
           print('could not open socket')
           sys.exit(1)

       fs = FramedStreamSock(s, debug=debug)

      # file = open("Text.txt","r")
      # r = file.read()
      # r = r.encode()

       file = open("Text2.txt", 'r')

       # r = file.read().split('\n')
       r = file.read()
       r = r.replace('\n', '\0')  # It is not accepting the \n so I switch it to null which is \0 and still be aware of where is the next line
       file.close()

       r = "Text2.txt" + '//NAME//' +" "+ r+" //FINISH!"  # I add this to send the name of the document attached to the file so we can put the same file name and I put this sign to show where I'll be separating this
       r = r.split(" ")
       #for x in r:
       #  Newr = x.encode()  # making the file in binary so I can send it


       #for x in range(len(Newr)):
        #   print("here")



       print("sending ",r)
       print("sending ", r)                 #Another call to see if works
       #print("sending hello world")
       #fs.sendmsg(b"hello world")
       Newr =''
       x = 0
       for x in range(len(r)):
           Newr += r[x]+" "
           if (x%100)==0:
               if x != 0:
                   print("This is Sending = ",Newr," AND X ",x)
                   fs.sendmsg(Newr.encode())
       #print("This is X",x," ",Newr)
       if (x+1) == len(r):
           #print("This is X!!!!!",x)
           print("This is Sending 2 =", Newr)
           fs.sendmsg(Newr.encode())

       print("received:", fs.receivemsg())
       #print("HERE")
       #fs.sendmsg(b"hello world")
       #print("received:", fs.receivemsg())

for i in range(2):
    ClientThread(serverHost, serverPort, debug)

