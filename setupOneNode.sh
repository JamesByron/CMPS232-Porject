#!/bin/bash
scp *.py pi@$1:DataArchiver/
ssh pi@$1 -tt <<EOF
sudo killall python3
sudo umount /dev/sda1
sudo killall hd-idle
sudo hd-idle/hd-idle -i 10
sudo mount /dev/sda1 /media/pi/
cd DataArchiver
python3 getCapacity.py /media/pi/
sudo umount /dev/sda1
exit
EOF