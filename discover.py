import threading
import time
import pygame
import subprocess 
import socket


ENABLE_DISCOVERY = True
MY_NAME = "PI Speakers"

def replyToDiscovery(sock3):
  print "some connection"
  a = sock3.recv(100);
  print "got something here = ", a
  if a == "hello":
    print "Discovery Successful!!"
    sock3.write("Hi my name is " + MY_NAME)

def EnableDiscovery():
  sock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock2.bind(('',9081))
  sock2.listen(1)
  while(True):
    connection, address = sock2.accept()
    replyToDiscovery(connection)

def startDiscovery():
  EnableDiscovery()

startDiscovery()