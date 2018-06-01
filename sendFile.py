import socket               # Import socket module
import testFile
import sys

#s = socket.socket()         # Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#host = socket.gethostname() # Get local machine name
host = sys.argv[2]
port = 12345                # Reserve a port for your service.

s.connect((host, port))
fileName = sys.argv[1] + " "
s.send(fileName.encode())
#s.send("Hello server!".encode())
f = open(sys.argv[1],'rb')
print('Sending...')
l = f.read(1024)
while (l):
    print('Sending...')
    s.send(l)
    l = f.read(1024)
f.close()
print("Done Sending")
s.shutdown(socket.SHUT_WR)
print(s.recv(1024).decode())
print(testFile.md5sum(sys.argv[1]))
s.close