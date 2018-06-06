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