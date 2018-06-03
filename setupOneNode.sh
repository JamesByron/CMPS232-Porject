#!/bin/bash
ssh pi@$1 <<EOF
sudo mount /dev/sda1 /media/pi/
cd DataArchiver
python3 getCapacity.py /media/pi/
sudo umount /dev/sda1
exit
EOF