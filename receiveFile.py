import socket               # Import socket module
import testFile
import os, sys

#s = socket.socket()         # Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = socket.gethostname() # Get local machine name
host = ""
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
space = " ".encode()
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    #os.system("sudo killall hd-idle")
    #os.system("sudo mount /dev/sda1 /media/pi/")
    print("Mounted hard drive")
    print("Receiving...")
    firstData = c.recv(1024)
    fileName = firstData[:firstData.find(space)]
    fileName = "/media/pi/" + fileName.decode()
    print(fileName)
    #f = open(fileName,'wb')
    totalSize = 0
    if len(firstData) > firstData.find(space)+1:
        totalSize += len(firstData) - firstData.find(space) - 1
    #    f.write(firstData[firstData.find(space)+1:])
    l = c.recv(1024)
    while (l):
        print("Receiving....")
        #f.write(l)
        totalSize += len(l)
        l = c.recv(1024)
    #f.close()
    print("Done Receiving")
    #checksum = testFile.md5sum(fileName)
    checksum = "hi"
    c.send(checksum.encode())
    c.close()
    print(totalSize)
    break
#os.system("sudo umount /dev/sda1")
#os.system("sudo ~/hd-idle/hd-idle -i 10")
