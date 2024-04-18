#!/usr/bin/python3

import socket
import time

tello_cmd_port =  8889
tello_cmd_ip = '192.168.1.69'

tello_cmd_add = (tello_cmd_ip,tello_cmd_port)

#------------------------------------------------------------------------------
if __name__=="__main__":
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # sock.sendto('command'.encode(encoding="utf-8"),tello_cmd_add)
  # sock.sendto('takeoff'.encode(encoding="utf-8"),tello_cmd_add)
  # time.sleep(7)
  # sock.sendto('land'.encode(encoding="utf-8"),tello_cmd_add)

  sock.sendto('command'.encode(encoding="utf-8"),tello_cmd_add)
  sock.sendto('takeoff'.encode(encoding="utf-8"),tello_cmd_add)
  time.sleep(4)  # Shortened sleep time to allow for yaw action
  print("wasa")
  sock.sendto('cw 90'.encode(encoding="utf-8"),tello_cmd_add)
  time.sleep(3)  # Allow some time for yaw action
  sock.sendto('land'.encode(encoding="utf-8"),tello_cmd_add)
  sock.close()
