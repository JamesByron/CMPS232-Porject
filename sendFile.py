import socket               # Import socket module
import testFile
import sys
import time

def sendOneFile(ip, location, fileName, transmitName, theEnd):
	repeats = 0
	#s = socket.socket()         # Create a socket object
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.settimeout(4)
	#host = socket.gethostname() # Get local machine name
	host = ip
	port = 12345
	while repeats < 5:
		try:
			s.connect((host, port))
			fn = transmitName + "  "
			s.send(fn.encode())
			if theEnd:
				print("Closing socket.")
				s.shutdown(socket.SHUT_WR)
				s.close
				return ("0",-1,0)
			rollingIndex = 0
			gigs = 1
			f = open(location+fileName,'rb')
			#print('Sending', fileName)
			startTime = time.time()
			l = f.read(4096)
			while (l):
				s.send(l)
				l = f.read(4096)
				rollingIndex += 1
				if rollingIndex == 250000:
					print(gigs,"GB")
					gigs += 1
					rollingIndex = 0
			f.close()
			endTime = time.time()
			s.shutdown(socket.SHUT_WR)
			localChecksum = testFile.md5sum(location+fileName)
			print("Awaiting checksum...")
			md5_cap = s.recv(4096).decode().split()
			s.close
			if (localChecksum == md5_cap[0]):
				return(md5_cap[0], md5_cap[1], endTime-startTime)
			else:
				print("Error sending ",fileName)
				repeats += 1
		except:
			repeats += 1
			print("Can't connect to",ip,". Tries left:",str(5-repeats))
			s.close()
			if repeats == 5:
				return ("0",-1,0)
			time.sleep(5)

#sendOneFile("192.168.0.2", "/media/james/Sandisk/", "VBox.log", "1")