import threading
import time
import pygame
import subprocess 
import socket

#Properties
WAIT_UNTIL_DATA = False
USING_PYGAME = False
USING_OMXPLAYER = True

#Globals
START_PLAYER = None
GETDATATHREAD = None
player = None
sock = None



def aplayer(): 
  file = "temp.mp3"
  #pygame.time.Clock().tick(100)
  pygame.mixer.music.stop()
  pygame.mixer.music.set_volume(1.0)
  pygame.mixer.music.load(file)
  pygame.mixer.music.play()
  print "Playing .."

def omxplayer():
  global player
  if player != None:
    player.stdin.write("q")
    player.kill()
    player = None
  player = subprocess.Popen(["omxplayer", "temp.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def init():
  print "Initializing Jukebox-pi..."
  global START_PLAYER
  if USING_PYGAME == True:
    pygame.init()
    pygame.mixer.init()
    START_PLAYER = aplayer
    print "Setting PYGAME as default player"
  elif USING_OMXPLAYER == True:
    START_PLAYER = omxplayer    
    print "Setting OMXPLAYER as default player"

def initsockets():
  global sock
  sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock.bind(('',8087))
  sock.listen(1)

def getData(connection):
  global f
  if f != None:
    f.close()
  f = open("temp.mp3","wb")
  f.write(connection.recv(38000))
  START_PLAYER()
  data = connection.recv(512)
  while len(data):
    f.write(data)
    data = connection.recv(512)

def startdatathread(connection):
  global GETDATATHREAD
  GETDATATHREAD = threading.Thread(target=someFunc)
  GETDATATHREAD.start()

init()
initsockets()


f = None
print "Jukebox-pi is good to go!"
while True:  
  connection, address = sock.accept()
  getData(connection)
