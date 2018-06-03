import os, sys

sysfs = os.statvfs(sys.argv[1])
cap = sysfs.f_bsize * sysfs.f_avail

return "startcapacity" + str(cap) + "endcapacity"