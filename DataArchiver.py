import os, sys
import subprocess
import fileinput
import time
import sendFile

#sysfs = os.statvfs("/media/pi/")
listNodes = []
filesStored = {}
maxNodes = 3
fileSequence = 1
totalDataSent = 0
receiveLogFile = open("receive_log","a")
verifyLogFile = open("verify_log","a")
filesDiretory = "/"

def getNewNode():
	assert(len(listNodes) < maxNodes)
	nextIP = "192.168.0." + str(2+len(listNodes))
	receiveLogFile.write("Adding_node "+nextIP+"\n")
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
	receiveLogFile.write("New_Node_Capacity "+str(nodeCapacity)+"\n")

def setupNewNode(ip):
	nextNode = "./setupOneNode.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	rv = call.communicate()[0].decode()
	rv = rv[rv.find("startcapacity")+13:rv.find("endcapacity")]
	nextNode = "./runRemote.sh " + ip
	call = subprocess.Popen(nextNode.split(),stdout=subprocess.PIPE)
	call.communicate()
	time.sleep(3)
	return int(rv)

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
	global fileSequence
	global maxNodes
	global totalDataSent
	global receiveLogFile
	global filesDiretory
	index = 0
	startTime = time.time()
	while len(files) > 0 and index < maxNodes:
		if index == len(listNodes):
			print("Out of capacity. Need to add more nodes.")
			getNewNode()
		elif files[0]["size"]+4096 < listNodes[index]["capacity"]:
			receiveLogFile.write("Storing_file "+files[0]["name"]+"\n")
			receiveLogFile.write("Storing_file_size "+str(files[0]["size"])+"\n")
			receiveLogFile.write("Storing_file_index "+str(fileSequence)+"\n")
			receiveLogFile.write("Storing_into_node "+str(index+1)+"\n")
			fileStartTime = time.time()
			aFile = files.pop(0)
			aFile["node"] = listNodes[index]["ip"]
			h, newCap = sendFile.sendOneFile(listNodes[index]["ip"], aFile["location"], aFile["name"],str(fileSequence))
			print("newCap ",newCap)
			aFile["hash"] = h
			#newCap = 0
			listNodes[index]["capacity"] = int(newCap)
			fileSequence += 1
			totalDataSent += files[0]["size"]
			receiveLogFile.write("File_transfer_time "+str(time.time()-fileStartTime)+"\n")
			receiveLogFile.write("Bytes_per_second "+str(files[0]["size"]/(time.time()-fileStartTime))+"\n")
			receiveLogFile.write("Total_transfer_time_taken "+str(time.time()-startTime)+"\n")
			receiveLogFile.write("Total_data_archived "+str(totalDataSent)+"\n")
		else:
			index += 1
		if len(files) == 0:
			files = getFiles(filesDiretory)
	receiveLogFile.write("Done_Archiving_Data\n\n")
	receiveLogFile.flush()

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

def main():
	global filesDiretory
	while True:
		i = input("Type new command:\nQuit: q\nVerify files: v\nShutdown nodes: s\nArchive files: a\nReset nodes: r\nUpload files: u\n")
		if i.strip() == "q" or i.strip() == "Q":
			verifyLogFile.close()
			receiveLogFile.close()
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
			print(len(fileList),"files found.")
			storeFiles(fileList)
		elif i.strip() == "v" or i.strip() == "V":
			verifyCluster()
		elif i.strip() == "u" or i.strip() == "U":
			os.system("./uploadFiles.sh")

main()