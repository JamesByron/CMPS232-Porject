import os, sys
import subprocess
import time

sysfs = os.statvfs("/media/pi/")
listNodes = []
filesStored = {}
maxNodes = 3

def getNewNode():
	assert(len(listNodes) < maxNodes)
	nextIP = "192.168.0." + str(2+len(listNodes))
	nextNode = "ping -W 1 -c 1 " + nextIP
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	returnValue = call.communicate()[0].decode()
	while ("1 received" not in returnValue):
		print("Node",len(listNodes),"is unavailable.  Plug it in now. Retrying in 5 seconds.")
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		time.sleep(5)
		returnValue = call.communicate()[0].decode()
	print("Found new node:",nextIP)
	newNode = {"ip": nextIP}
	nodeCapacity = setupNewNode(nextIP)
	newNode["capacity"] = nodeCapacity

def setupNewNode(ip):
	nextNode = "./setupOneNoede.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode()
	rv = rv[rv.find("startcapacity")+13:rv.find("endcapacity")]
	return int(rv)


def setupCluster():
	#os.system("./setup.sh")
	os.system("./uploadFiles.sh")

def main():
	getNewNode()

main()