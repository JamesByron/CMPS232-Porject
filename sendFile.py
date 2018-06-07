import socket               # Import socket module
import testFile
import sys

def sendOneFile(ip, location, fileName, transmitName):
	repeats = 0
	while repeats < 5:
		#s = socket.socket()         # Create a socket object
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#host = socket.gethostname() # Get local machine name
		host = ip
		port = 12345
		s.connect((host, port))
		fn = transmitName + "  "
		s.send(fn.encode())
		f = open(location+fileName,'rb')
		print('Sending', fileName)
		l = f.read(1024)
		while (l):
		    s.send(l)
		    l = f.read(1024)
		f.close()
		s.shutdown(socket.SHUT_WR)
		md5_cap = s.recv(1024).decode().split()
		s.close
		if (testFile.md5sum(location+fileName) == md5_cap[0]):
			return(md5_cap[0], md5_cap[1])
		else:
			print("Error sending ",fileName)
			repeats += 1

#sendOneFile("192.168.0.2", "/media/james/Sandisk/", "VBox.log", "1")