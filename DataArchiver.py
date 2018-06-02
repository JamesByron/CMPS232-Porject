import os, sys
import subprocess

sysfs = os.statvfs("/")
listNodes = []
maxNodes = 3

def getNewNode():
	assert(len(listNodes) < maxNodes)
	next = "ping -W 1 -c 1 192.168.0." + str(2-len(listNodes))
	call = subprocess.Popen(next.split(),stdout=subprocess.PIPE)
	returnValue = call.communicate()[0].decode()
	print(returnValue)
	print("1 received" in returnValue)

getNewNode()

