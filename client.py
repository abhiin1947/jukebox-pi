import threading
import time
import pygame

def aplayer( sock ): 
  file = "temp.mp3"
  #pygame.time.Clock().tick(100)
  pygame.mixer.music.stop()
  pygame.mixer.music.load(file)
  pygame.mixer.music.play()
  print "Playing .."

import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(('',8087))
sock.listen(1)
pygame.init()
pygame.mixer.init()
f = None
while True:
  connection, address = sock.accept()
  if f != None:
    f.close()
  f = open("temp.mp3","wb")
  f.write(connection.recv(38000))
  aplayer(connection)
  data = connection.recv(512)
  while len(data):
    f.write(data)
    data = connection.recv(512)
#  while STATE == "playing":
#    time.sleep(1)
    
