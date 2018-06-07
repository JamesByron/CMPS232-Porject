#!/bin/bash
ssh pi@$1 -tt <<EOF
sudo killall python3
sudo umount /dev/sda1
sudo mount /dev/sda1 /media/pi/
cd DataArchiver
touch FileNames
nohup python3 receiveFile.py FileNames verify &
exit
EOF