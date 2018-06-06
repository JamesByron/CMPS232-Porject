import os, sys
import subprocess
import fileinput
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

def setupNewNode(ip):
	nextNode = "./setupOneNode.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode()
	rv = rv[rv.find("startcapacity")+13:rv.find("endcapacity")]
	return int(rv)

def setupCluster():
	os.system("./setup.sh")

def getFiles(location):
	call = subprocess.Popen(["ls","-l",location],stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode().split("\n")
	firstList = [f.split() for f in rv]
	returnList = []
	for each in firstList:
		if len(each) > 2:
			n = each[8]
			if len(each) > 9:
				for s in each[9:]:
					n+=" "+s
			if each[0][0] == "-" and int(each[4]) > 0:
				returnList.append({"size": int(each[4]),"location": location,"name": n.replace("\'","")})
			elif each[0][0] == "d":
				returnList += getFiles(location+n.replace("\'","")+"/")
	return returnList

def storeFiles(files):
	while len(files) > 0:
		index = 0
		if index == len(listNodes):
			print("Out of capacity. Need to add more nodes.")
			getNewNode()
		elif files[0]["size"]+4096 < listNodes[index]["capacity"]:
			aFile = files.pop(0)
			aFile["node"] = listNodes[index]["ip"]
			h, newCap = sendFile.sendOneFile(listNodes[index]["ip"], aFile["location"], aFile["name"])
			aFile["hash"] = h
			listNodes[index]["capacity"] = int(newCap)
			#exit()
		else:
			index += 1

def main():
	i = input("Type new command:\nQuit: q\nRetrieve files: r\nSetup all nodes: s\nArchive files: a\nReset nodes: d")
	if i.strip() == "q" or i.strip() == "Q":
		exit()
	elif i.strip() == "r" or i.strip() == "R":
		while True
			x = input("Enter file name to retrieve or \"quit\" when finished. ")
			if x.strip() == "quit":
				break
	elif i.strip() == "s" or i.strip() == "S":
		setupCluster()
	elif i.strip() == "a" or i.strip() == "A":
		x = input("Directory with files to archive is /media/james/Sandisk/. Type full path to change or press enter to use default.")
		if x == "":
			originDirectory = "/media/james/Sandisk/"
		else:
			originDirectory = x
		fileList = getFiles(originDirectory)
		print(len(fileList),"files found.")
		storeFiles(fileList)
	elif i.strip() == "d" or i.strip() == "D":
		pass
	#need to finish d r 

main()