import os, sys
import subprocess
import time
import sendFile

#sysfs = os.statvfs("/media/pi/")
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
		print("Node",len(listNodes)+1,"is unavailable.  Plug it in now. Retrying in 5 seconds.")
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		time.sleep(5)
		returnValue = call.communicate()[0].decode()
	print("Found new node:",nextIP)
	newNode = {"ip": nextIP}
	nodeCapacity = setupNewNode(nextIP)
	newNode["capacity"] = nodeCapacity
	listNodes.append(newNode)
	print(nodeCapacity)

def setupNewNode(ip):
	nextNode = "./setupOneNode.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode()
	rv = rv[rv.find("startcapacity")+13:rv.find("endcapacity")]
	return int(rv)

def setupCluster():
	#os.system("./setup.sh")
	#os.system("./uploadFiles.sh")
	pass

def getFiles(location):
	call = subprocess.Popen(("ls -l " + location).split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode().split("\n")
	firstList = [f.split() for f in rv]
	returnList = []
	for each in firstList:
		if len(each) > 2:
			returnList.append({"size": int(each[4]),"location": location,"name": each[8]}) if int(each[4]) > 0 else None
	return returnList

def storeFiles(files):
	#print(files)
	while len(files) > 0:
		index = 0
		if index == len(listNodes):
			print("Out of capacity. Need to add more nodes.")
			getNewNode()
		elif files[0]["size"]+4096 < listNodes[index]["capacity"]:
			aFile = files.pop(0)
			newCap = sendFile.sendOneFile(listNodes[index]["ip"], aFile["location"], aFile["name"])
			listNodes[index]["capacity"] = newCap
		else:
			index += 1

def main():
	setupCluster()
	#getNewNode()
	originDirectory = "/media/james/Sandisk/"
	#originDirectory = "/home/james/ds/"
	fileList = getFiles(originDirectory)
	storeFiles(fileList)

main()