import os, sys
import subprocess
import fileinput
import time
import sendFile

#sysfs = os.statvfs("/media/pi/")
listNodes = []
maxNodes = 3
fileSequence = 1
totalDataSent = 0
filesDiretory = "/"

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
	newNode = {"ip":nextIP, "Active":True}
	#nodeCapacity = 100000000000
	nodeCapacity = setupNewNode(nextIP)
	newNode["capacity"] = nodeCapacity
	listNodes.append(newNode)

def setupNewNode(ip):
	nextNode = "./setupOneNode.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode()
	rv = rv[rv.find("startcapacity")+13:rv.find("endcapacity")]
	nextNode = "./runRemote.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	x = call.communicate()[0].decode()
	#print(x)
	time.sleep(3)
	#print("rv", rv)
	#rv = 1000000000
	return int(rv)

def getFiles(location):
	call = subprocess.Popen(["ls","-l",location],stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode().split("\n")
	firstList = [f.split() for f in rv]
	returnList = []
	for each in firstList:
		if len(each) > 2 and len(each) < 10:
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
	global fileSequence
	global maxNodes
	global totalDataSent
	global filesDiretory
	receiveLogFile = open("receive_log_master","a")
	receiveLogFile.write("Storing_file\tStoring_file_size\tStoring_file_index\tStoring_into_node\tFile_transfer_time\tBytes_per_second\tTotal_time_taken\tTotal_data_archived\tNode_capacity\n")
	index = 0
	startTime = time.time()
	while len(files) > 0 and index < maxNodes:
		if index == len(listNodes):
			print("Out of capacity. Need to add more nodes.")
			getNewNode()
			time.sleep(2)
		elif files[0]["size"]+100000000 < listNodes[index]["capacity"]:
			receiveLogFile.write(files[0]["name"]+"\t")
			receiveLogFile.write(str(files[0]["size"])+"\t")
			receiveLogFile.write(str(fileSequence)+"\t")
			receiveLogFile.write(str(index+1)+"\t")
			aFile = files.pop(0)
			aFile["node"] = listNodes[index]["ip"]
			h, newCap, tToken = sendFile.sendOneFile(listNodes[index]["ip"], aFile["location"], aFile["name"],str(fileSequence),False)
			print("newCap ",newCap)
			aFile["hash"] = h
			#newCap = 0
			listNodes[index]["capacity"] = int(newCap)
			fileSequence += 1
			totalDataSent += aFile["size"]
			receiveLogFile.write(str(tToken)+"\t")
			stringToWrite = str(aFile["size"]/tToken) if tToken > 0 else "0"
			receiveLogFile.write(stringToWrite+"\t")
			receiveLogFile.write(str(time.time()-startTime)+"\t")
			receiveLogFile.write(str(totalDataSent)+"\t")
			receiveLogFile.write(str(newCap)+"\n")
		elif listNodes[index]["capacity"] == -1:
			h, newCap, tToken = sendFile.sendOneFile(listNodes[index]["ip"], "end", "end","end",True)
			time.sleep(5)
			nextNode = "./restart.sh " + listNodes[index]["ip"]
			call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
			call.communicate()
			listNodes.pop(index)
			time.sleep(30)
			getNewNode()
			time.sleep(3)
		else:
			h, newCap, tToken = sendFile.sendOneFile(listNodes[index]["ip"], "end", "end","end",True)
			index += 1
		if len(files) == 0:
			files = getFiles(filesDiretory)
	receiveLogFile.write("Done_Archiving_Data\n\n")

def resetCluster():
	ipValue = 2
	while (ipValue <= 4):
		nextIP = "192.168.0." + str(ipValue)
		nextNode = "ping -W 1 -c 1 " + nextIP
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		returnValue = call.communicate()[0].decode()
		while ("1 received" not in returnValue):
			print("Node",ipValue-1,"is unavailable.  Plug it in now. Retrying in 5 seconds.")
			call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
			time.sleep(5)
			returnValue = call.communicate()[0].decode()
		nextNode = "./reset.sh " + nextIP
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		call.communicate()
		ipValue += 1

def verifyCluster():
	verifyLogFile = open("verify_log_master","a")
	ipValue = 2
	startTime = time.time()
	verifyLogFile.write("Starting_verifyCluster "+str(startTime)+"\n")
	while (ipValue <= 4):
		nextIP = "192.168.0." + str(ipValue)
		nextNode = "ping -W 1 -c 1 " + nextIP
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		returnValue = call.communicate()[0].decode()
		while ("1 received" not in returnValue):
			print("Node",ipValue-1,"is unavailable.  Plug it in now. Retrying in 5 seconds.")
			call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
			time.sleep(5)
			returnValue = call.communicate()[0].decode()
		nextNode = "./verify.sh " + nextIP
		call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
		call.communicate()
		ipValue += 1
	verifyLogFile.close()

def main():
	global filesDiretory
	while True:
		i = input("Type new command:\nQuit: q\nVerify files: v\nShutdown nodes: s\nArchive files: a\nReset nodes: r\nUpload files: u\n")
		if i.strip() == "q" or i.strip() == "Q":
			exit()
		elif i.strip() == "r" or i.strip() == "R":
			resetCluster()
		elif i.strip() == "s" or i.strip() == "S":
			os.system("./shutdown.sh")
		elif i.strip() == "a" or i.strip() == "A":
			x = input("Directory with files to archive is /media/james/Sandisk/. Type full path to change or press enter to use default.")
			if x == "":
				originDirectory = "/media/james/Sandisk/"
			else:
				originDirectory = x
			filesDiretory = originDirectory
			fileList = getFiles(originDirectory)
			storeFiles(fileList)
		elif i.strip() == "v" or i.strip() == "V":
			verifyCluster()
		elif i.strip() == "u" or i.strip() == "U":
			os.system("./uploadFiles.sh")

main()