import socket
import testFile
import os, sys
import subprocess
import time

fileList = []
fileNames = {}

def receiveLoop():
    #s = socket.socket()         # Create a socket object
    global fileList
    global fileNames
    receiveLog = open("receive_log","a")
    receiveLog.write("Start_receiveLoop\tGot_connection_time\tFile_Name\tDone_Receiving\tTransfer_Time\tBytes_received\tBytes_per_second\tCombined_size\tChecksum_time\tType\n")
    receiveLoopStartTime = time.time()
    combinedSize = 0
    killString = ("sudo killall hd-idle").split()
    runString = ("sudo ~/hd-idle/hd-idle -i 10").split()
    mountString = ("sudo mount /dev/sda1 /media/pi/").split()
    umountString = ("sudo umount /dev/sda1").split()
    call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
    call.communicate()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(4)
    #host = socket.gethostname() # Get local machine name
    host = ""
    port = 12345
    s.bind((host, port))        # Bind to the port
    space = "  ".encode()
    s.listen(5)                 # Now wait for client connection.
    capacityAvailable = 0
    listDestination = "FileNames" if len(sys.argv) < 2 else sys.argv[1]
    f2 = open(listDestination,"a")
    while True:
        try:
            c, addr = s.accept()
            #print('Got_connection_from',addr)
            startTime = time.time()
            #call = subprocess.Popen(killString,stdout=subprocess.PIPE)
            #call.communicate()
            firstData = c.recv(4096)
            fileName = firstData[:firstData.find(space)].decode()
            receiveLog.write(str(receiveLoopStartTime)+"\t")
            if fileName == "end":
                receiveLog.write(str(time.time())+"\n")
                print("End")
                break
            receiveLog.write(str(startTime)+"\t")
            receiveLog.write(fileName+"\t")
            fileName = "/media/pi/" + fileName
            f = open(fileName,'wb')
            totalSize = 0
            if len(firstData) > firstData.find(space)+2:
                totalSize += len(firstData) - firstData.find(space) - 2
            f.write(firstData[firstData.find(space)+2:])
            l = c.recv(4096)
            while (l):
                f.write(l)
                totalSize += len(l)
                l = c.recv(4096)
            f.close()
            endTime = time.time()
            receiveLog.write(str(endTime)+"\t")
            receiveLog.write(str(endTime-startTime)+"\t")
            receiveLog.write(str(totalSize)+"\t")
            receiveLog.write(str(totalSize/(endTime-startTime))+"\t")
            capacityAvailable = getCapacity()
            checksum = testFile.md5sum(fileName)
            checksumTime = time.time()
            c.send((checksum + " " + str(capacityAvailable)).encode())
            c.close()
            combinedSize += totalSize
            receiveLog.write(str(combinedSize)+"\t")
            receiveLog.write(str(checksumTime-endTime)+"\t")
            fileDict = {"name":fileName,"hash":checksum,"size":totalSize,"level":0}
            if fileName not in fileNames:
                fileNames[fileName] = len(fileList)
                fileList.append(fileDict)
                receiveLog.write("NewFile\n")
            else:
                receiveLog.write("Retransmit\n")
                fileList[fileNames[fileName]] = fileDict
            line = fileDict["name"]+"  "+fileDict["hash"]+"  "+str(fileDict["size"])+"  "+str(fileDict["level"])+"\n"
            f2.write(line)
            #f2.flush()
            #receiveLog.flush()
            #time.sleep(1)
            #call = subprocess.Popen(runString,stdout=subprocess.PIPE)
            #call.communicate()
        except Exception as inst:
            receiveLog.write("Error\n")
            print(type(inst))
            print(inst.args)
            print(inst)
    s.close()
    call = subprocess.Popen(umountString,stdout=subprocess.PIPE)
    call.communicate()
    f2.close()
    receiveLog.close()

def getCapacity():
    sysfs = os.statvfs("/media/pi/")
    cap = sysfs.f_bsize * sysfs.f_bavail
    return cap

def getFileList():
    global fileList
    global fileNames
    f = open(sys.argv[1],"r")
    for line in f:
        aFile = (line.strip().split("  "))
        fileDict = {"name": aFile[0], "hash": aFile[1], "size": int(aFile[2]), "level": int(aFile[3])}
        if aFile[0] not in fileNames:
            fileNames[aFile[0]] = len(fileList)
            fileList.append(fileDict)
        else:
            fileList[fileNames[aFile[0]]] = fileDict
    f.close()

def writeFileList():
    global fileList
    global fileNames
    listDestination = "FileNames" if len(sys.argv) < 2 else sys.argv[1]
    f = open(listDestination, "w")
    for each in fileList:
        line = each["name"]+"  "+each["hash"]+"  "+str(each["size"])+"  "+str(each["level"])+"\n"
        f.write(line)
    f.close()       

def verifyFiles():
    global fileList
    global fileNames
    logFile = open("verify_log","a")
    logFile.write("Start_verifying\tFile_corrupted\tFile_name\tNumber_files_verified\tTotal_corrupted_files\tTime_to_verify\n")
    corruptedFiles = 0
    startTime = time.time()
    mountString = ("sudo mount /dev/sda1 /media/pi/").split()
    umountString = ("sudo umount /dev/sda1").split()
    call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
    call.communicate()
    for each in fileList:
        aList = each.strip().split("  ")
        checksum = testFile.md5sum(aList[0])
        result = checksum == aList[1]
        logFile.write(str(startTime)+"\t")
        if not result:
            logFile.write("Yes\t")
            corruptedFiles += 1
        else:
            logFile.write("No\t")
        logFile.write(aList[0]+"\t")
        logFile.write(str(len(fileList))+"\t")
        logFile.write(str(corruptedFiles)+"\t")
        logFile.write(str(time.time()-startTime)+"\t")
    call = subprocess.Popen(umountString,stdout=subprocess.PIPE)
    call.communicate()
    logFile.close()

def main():
    if len(sys.argv) > 1:
        getFileList()
    if len(sys.argv) > 2:
        verifyFiles()
    else:
        receiveLoop()

main()