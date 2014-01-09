import threading
import time
import pygame
import subprocess 
import socket

#Properties
WAIT_UNTIL_DATA = False
USING_PYGAME = False
USING_OMXPLAYER = True
ENABLE_DISCOVERY = True

#Globals
START_PLAYER = None
GETDATATHREAD = None
MY_NAME = "PI Speakers"
player = None
sock = None

def replyToDiscovery(sock):
  print "some connection"
  a = sock.recv(100);
  print "got something here = ", a
  if a == "hello":
    print "Discovery Successful!!"
    sock.write("Hi my name is " + MY_NAME)

def EnableDiscovery():
  sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  sock.bind(('',9081))
  sock.listen(10)
  while(True):
    connection, address = sock.accept()
    t1 = threading.Thread(target=replyToDiscovery, args = (connection,))
    t1.start()

def startDiscovery():
  t1 = threading.Thread(target=EnableDiscovery)
  t1.start()  

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
    try:
      player.stdin.write("q")
    except:
      pass
    player.kill()
    player = None
  player = subprocess.Popen(["omxplayer", "temp.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  print "Playing .."

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

if ENABLE_DISCOVERY:
  startDiscovery()

f = None
print "Jukebox-pi is good to go!"
while True:  
  connection, address = sock.accept()
  getData(connection)
