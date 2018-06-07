import socket               # Import socket module
import testFile
import os, sys
import subprocess
import time

fileList = []
fileNames = {}

def receiveLoop():
    #s = socket.socket()         # Create a socket object
    receiveLoopStartTime = time.time()
    logFile = open("receive_log","a")
    logFile.write("Start_receiveLoop "+ str(time.time())+"\n")
    combinedSize = 0
    killString = ("sudo killall hd-idle").split()
    runString = ("sudo ~/hd-idle/hd-idle -i 10").split()
    mountString = ("sudo mount /dev/sda1 /media/pi/").split()
    umountString = ("sudo umount /dev/sda1").split()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = socket.gethostname() # Get local machine name
    host = ""
    port = 12345                 # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port
    space = "  ".encode()
    s.listen(5)                 # Now wait for client connection.
    capacityAvailable = 0
    listDestination = "FileNames" if len(sys.argv) < 2 else sys.argv[1]
    f2 = open(listDestination,"a")
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got_connection_from',addr)
        logFile.write("Got_connection_time "+str(time.time())+"\n")
        startTime = time.time()
        #call = subprocess.Popen(killString,stdout=subprocess.PIPE)
        #call.communicate()
        firstData = c.recv(1024)
        fileName = firstData[:firstData.find(space)]
        if fileName == "end":
            logFile.write("end "+str(time.time())+"\n")
            logFile.close()
            c.close()
            break
        logFile.write("Receiving_file_current_time "+str(time.time())+"\n")
        call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
        call.communicate()
        fileName = "/media/pi/" + fileName.decode()
        f = open(fileName,'wb')
        totalSize = 0
        if len(firstData) > firstData.find(space)+2:
            totalSize += len(firstData) - firstData.find(space) - 2
        f.write(firstData[firstData.find(space)+2:])
        l = c.recv(1024)
        while (l):
            f.write(l)
            totalSize += len(l)
            l = c.recv(1024)
        f.close()
        logFile.write("Done_Receiving "+str(time.time())+"\n")
        logFile.write("Transfer_Time "+ str(time.time()-startTime)+"\n")
        logFile.write("Bytes_received "+str(totalSize)+"\n")
        logFile.write("Bytes_per_second "+str(totalSize/(time.time()-startTime))+"\n")
        capacityAvailable = getCapacity()
        checksum = testFile.md5sum(fileName)
        c.send((checksum + " " + str(capacityAvailable)).encode())
        c.close()
        combinedSize += totalSize
        logFile.write("Combined_size "+str(combinedSize)+"\n")
        fileDict = {"name":fileName,"hash":checksum,"size":totalSize,"level":0}
        if fileName not in fileNames:
            fileNames[fileName] = len(fileList)
            fileList.append(fileDict)
        else:
            logFile.write("Retransmitted "+fileName+"\n")
            fileList[fileNames[fileName]] = fileDict
        line = fileDict["name"]+"  "+fileDict["hash"]+"  "+str(fileDict["size"])+"  "+str(fileDict["level"])+"\n"
        f2.write(line)
        f2.flush()
        time.sleep(1)
        #call = subprocess.Popen(runString,stdout=subprocess.PIPE)
        #call.communicate()
        call = subprocess.Popen(umountString,stdout=subprocess.PIPE)
        call.communicate()
        logFile.flush()
    s.close()
    f2.close()
    logFile.write("Exit_receiveLoop_function "+str(time.time()-receiveLoopStartTime)+"\n")
    logFile.close()

def getCapacity():
    sysfs = os.statvfs("/media/pi/")
    cap = sysfs.f_bsize * sysfs.f_bavail
    return cap

def getFileList():
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
    listDestination = "FileNames" if len(sys.argv) < 2 else sys.argv[1]
    f = open(listDestination, "w")
    for each in fileList:
        line = each["name"]+"  "+each["hash"]+"  "+str(each["size"])+"  "+str(each["level"])+"\n"
        f.write(line)
    f.close()       

def verifyFiles():
    logFile = open("verify_log","a")
    corruptedFiles = 0
    startTime = time.time()
    mountString = ("sudo mount /dev/sda1 /media/pi/").split()
    umountString = ("sudo umount /dev/sda1").split()
    call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
    call.communicate()
    logFile.write("Start_verifying "+str(time.time())+"\n")
    for each in fileList:
        aList = each.strip().split("  ")
        checksum = testFile.md5sum(aList[0])
        result = checksum == aList[1]
        if not result:
            logFile.write("File_corrupted "+aList[0]+"\n")
            corruptedFiles += 1
    logFile.write("Number_files_verified "+str(len(fileList))+"\n")
    logFile.write("Total_corrupted_files "+str(corruptedFiles)+"\n")
    logFile.write("Time_to_verify "+str(time.time()-startTime)+"\n")
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