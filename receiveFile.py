import socket               # Import socket module
import testFile
import os, sys
import subprocess
import time

def receiveLoop():
    #s = socket.socket()         # Create a socket object
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
        print('Got connection from', addr)
        #call = subprocess.Popen(killString,stdout=subprocess.PIPE)
        #call.communicate()
        call = subprocess.Popen(mountString,stdout=subprocess.PIPE)
        call.communicate()
        print("Mounted hard drive")
        print("Receiving...")
        firstData = c.recv(1024)
        fileName = firstData[:firstData.find(space)]
        fileName = "/media/pi/" + fileName.decode()
        f = open(fileName,'wb')
        totalSize = 0
        if len(firstData) > firstData.find(space)+1:
            totalSize += len(firstData) - firstData.find(space) - 1
        f.write(firstData[firstData.find(space)+1:])
        l = c.recv(1024)
        while (l):
            print("Receiving....")
            f.write(l)
            totalSize += len(l)
            l = c.recv(1024)
        f.close()
        print("Done Receiving")
        capacityAvailable = getCapacity()
        checksum = testFile.md5sum(fileName)
        c.send((checksum + " " + str(capacityAvailable)).encode())
        c.close()
        print(totalSize)
        time.sleep(1)
        #call = subprocess.Popen(runString,stdout=subprocess.PIPE)
        #call.communicate()
        call = subprocess.Popen(umountString,stdout=subprocess.PIPE)
        call.communicate()
        

def getCapacity():
    sysfs = os.statvfs("/media/pi/")
    cap = sysfs.f_bsize * sysfs.f_bavail
    return cap

receiveLoop()