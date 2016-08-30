#!/usr/bin/env python

import socket
import subprocess
import sys
from datetime import datetime

subprocess.call ('clear', shell=True)

host = raw_input ("Enter IP of scanning hosts: ")

print "-"*60
print "Scanning remote host", host
print "-"*60


tl=datetime.now()

try:
        for port in range(1,1025):
                sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                result=sock.connect_ex((host,port))
                if result == 0:
                        print "Port {}:\t Open".format(port)
                sock.close()
except KeyboardInterrupt:
        print "You pressed Ctrl+C"
        sys.exit()


except socket.error:
        print "Couldn't connect to server"
        sys.exit()

t2=datatume.now()
total=t1-t2

print 'Scanning complited in: ', total
