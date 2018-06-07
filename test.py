import fileinput
import sys

i = input("hello ")
print(type(i))

print(i=="")
fileList = []
f = open(sys.argv[1],"r")
for line in f:
	print(line.strip())

#1) Check that rode is up
#2) Set up the one node only
#3) Upload ifles to that node
#4) Run the receive script