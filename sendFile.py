import socket               # Import socket module
import testFile
import sys

def sendOneFile(ip, location, fileName):
	#s = socket.socket()         # Create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#host = socket.gethostname() # Get local machine name
	host = ip
	port = 12345                # Reserve a port for your service.
	s.connect((host, port))
	fn = fileName + "  "
	s.send(fn.encode())
	f = open(location+fileName,'rb')
	print('Sending...')
	l = f.read(1024)
	while (l):
	    print('Sending....')
	    s.send(l)
	    l = f.read(1024)
	f.close()
	print("Done Sending")
	s.shutdown(socket.SHUT_WR)
	md5_cap = s.recv(1024).decode().split()
	s.close
	#print(md5_cap)
	print(testFile.md5sum(location+fileName) == md5_cap[0])
	return(md5_cap[1])