import socket               # Import socket module
import testFile
import os, sys
import subprocess
import time

def receiveLoop():
    #s = socket.socket()         # Create a socket object
    print("Start_receiveLoop",(time.time()))
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
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got_connection_from', addr)
        print("Got_connection_time",(time.time()))
        startTime = time.time()
        #call = subprocess.Popen(killString,stdout=subprocess.PIPE)
        #call.communicate()
        call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
        call.communicate()
        firstData = c.recv(1024)
        fileName = firstData[:firstData.find(space)]
        print("Receiving_file_time",time.time())
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
        print("Done_Receiving",time.time())
        print("Transfer_Time",time.time()-startTime)
        capacityAvailable = getCapacity()
        checksum = testFile.md5sum(fileName)
        c.send((checksum + " " + str(capacityAvailable)).encode())
        c.close()
        print("Bytes_received",totalSize)
        combinedSize += totalSize
        print("Combined_size",combinedSize)
        time.sleep(1)
        #call = subprocess.Popen(runString,stdout=subprocess.PIPE)
        #call.communicate()
        call = subprocess.Popen(umountString,stdout=subprocess.PIPE)
        call.communicate()
        break
    s.close()
        

def getCapacity():
    sysfs = os.statvfs("/media/pi/")
    cap = sysfs.f_bsize * sysfs.f_bavail
    return cap

receiveLoop()