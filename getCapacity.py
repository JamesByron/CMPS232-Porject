import os, sys

sysfs = os.statvfs(sys.argv[1])
cap = sysfs.f_bsize * sysfs.f_bavail

print("startcapacity" + str(cap) + "endcapacity")