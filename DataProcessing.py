import os, sys

#fileNames = []
fileSizes = {}
receiveLog = []
receiveLogMaster = []
initialSetupTime = []
busyness = {}
speed = {}
verify = {}

# Destination_file_name	Checksum	Size	Priority	Node
fileNamesFile = open("data/FileNames_combined.tsv","r")
firstLine = True
#1) Chart showing the sizes and number of files as a x-log scale bar chart
for line in fileNamesFile:
	if not firstLine:
		aLine = line.split()
		size = int(aLine[2])
		if size not in fileSizes:
			fileSizes[size] = 1
		else:
			fileSizes[size] += 1
	else:
		firstLine = False
fileNamesFile.close()

fileSizesOutput = open("data/FileSizes.tsv","w")
fileSizesOutput.write("Size\tCount\n")
for key in sorted(fileSizes.keys()):
	fileSizesOutput.write(str(key) + "\t" + str(fileSizes[key]) + "\n")
fileSizesOutput.close()

firstLine = True
# Start_receiveLoop	Got_connection_time	File_Name	Done_Receiving	Transfer_Time	Bytes_received	Bytes_per_second	Combined_size	Checksum_time	Type	Node
receiveLogFile = open("data/receive_log_combined.tsv","r")
#Start_receiveLoop: StartLoop 0
#Got_connection_time: GotConn 1
#File_Name: Name 2
#Done_Receiving: Done 3
#Transfer_Time: TransTime 4
#Bytes_received: Bytes 5
#Bytes_per_second: BPS 6
#Combined_size: TotalSize 7
#Node: Node 10

for each in receiveLogFile:
	line = each.split()
	if not firstLine and len(line) > 3:
		d = {}
		d["StartLoop"] = float(line[0])
		d["GotConn"] = float(line[1])
		d["Name"] = line[2]
		d["Done"] = float(line[3])
		d["TransTime"] = float(line[4])
		d["Bytes"] = int(line[5])
		d["BPS"] = float(line[6])
		d["TotalSize"] = int(line[7])
		d["Node"] = line[10]
		#if len(receiveLog) == 0 or d["Node"] != receiveLog[len(receiveLog)-1]["Node"]:
		receiveLog.append(d)
	else:
		firstLine = False
receiveLogFile.close()
firstLine = True

# Storing_file	Storing_file_size	Storing_file_index	Storing_into_node	File_transfer_time	Bytes_per_second	Total_time_taken	Total_data_archived	Node_capacity
receiveLogMasterFile = open("data/receive_log_master.tsv","r")

# Storing_file_size: Size 1
# Storing_file_index: Name 2
# Storing_into_node: Node 3
# File_transfer_time: TransTime: 4
# Bytes_per_second: BPS 5
# Total_time_taken: TotalTime 6
# Total_data_archived: TotalData 7

for each in receiveLogMasterFile:
	line = each.split()
	if not firstLine and len(line) > 1:
		d = {}
		d["Size"] = int(line[1])
		d["Name"] = line[2]
		d["Node"] = line[3]
		d["TransTime"] = float(line[4])
		d["BPS"] = float(line[5])
		d["TotalTime"] = float(line[6])
		d["TotalData"] = int(line[7])
		prev = 0 if len(receiveLogMaster) == 0 else receiveLogMaster[len(receiveLogMaster)-1]["TotalTime"]
		if len(receiveLogMaster) == 0 or d["Node"] != receiveLogMaster[len(receiveLogMaster)-1]["Node"]:
			# master: initial setup time for a node
			initialSetupTime.append(d["TotalTime"]-prev)
		else:
			# master: total time vs transfer time by file size: busyness
			totalT = d["TotalTime"] - prev
			busyT = d["TransTime"] / totalT
			if d["Size"] not in busyness:
				busyness[d["Size"]] = {"busyT": busyT,"num": 1}
			else:
				busyness[d["Size"]]["num"] += 1
				busyness[d["Size"]]["busyT"] += busyT
		# master: BPS vs file size
		if d["Size"] not in speed:
			speed[d["Size"]] = {"BPS": d["BPS"], "num": 1}
		else:
			speed[d["Size"]]["BPS"] += d["BPS"]
			speed[d["Size"]]["num"] += 1
		receiveLogMaster.append(d)
	else:
		firstLine = False

receiveLogMasterFile.close()

# sort busyness by file size, write it out
newBusyness = {}
for key in busyness:
	newBusyness[key] = busyness[key]["busyT"] / busyness[key]["num"]

newSpeed = {}
for key in speed:
	newSpeed[key] = speed[key]["BPS"] / speed[key]["num"]

busynessFile = open("data/busyness.tsv","w")
busynessFile.write("Size\tTransferToTotalTime\n")
for key in sorted(newBusyness.keys()):
	busynessFile.write(str(key) + "\t" + str(newBusyness[key]) + "\n")

busynessFile.close()

speedFile = open("data/speed.tsv","w")
speedFile.write("Size\tAvgBPS\n")
for key in sorted(newSpeed.keys()):
	speedFile.write(str(key) + "\t" + str(newSpeed[key]) + "\n")

speedFile.close()

firstLine = True
# Start_verifying	File_corrupted	File_name	File_size	Number_files_verified	Total_corrupted_files	Total_time	Time_to_verify
verifyFile = open("data/verify_log_combined.tsv","r")

for each in verifyFile:
	if not firstLine:
		line = each.split()
		s = int(line[3])
		t = float(line[7])
		if s not in verify:
			verify[s] = {"busyT": t, "num": 1}
		else:
			verify[s]["num"] += 1
			verify[s]["busyT"] += t
	else:
		firstLine = False

verifyFile.close()
newVerify = {}
for key in verify:
	newVerify[key] = verify[key]["busyT"] / verify[key]["num"]

#file size vs verification time
#is growth linear?
# something for verification too
verifyTimeFile = open("data/verify.tsv","w")
verifyTimeFile.write("Size\tTimeToVerify\n")
for key in sorted(newVerify.keys()):
	verifyTimeFile.write(str(key) + "\t" + str(newVerify[key]) + "\n")

verifyTimeFile.close()
print("Initial setup time")
print("Node 1",initialSetupTime[0])
print("Node 2",initialSetupTime[1])
print("Node 3",initialSetupTime[2])
