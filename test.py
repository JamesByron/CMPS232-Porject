import fileinput
import sys

i = input("hello ")
print(type(i))

print(i=="")
fileList = []

if (len(sys.argv) > 1):
	f = fileinput.input()
	for line in f:
		fileList.append(line.strip().split())
print(fileList)
{"name": "name", "hash": "hash", "size": 0, "level": 0}

1) Check that rode is up
2) Set up the one node only
3) Upload ifles to that node
4) Run the receive script