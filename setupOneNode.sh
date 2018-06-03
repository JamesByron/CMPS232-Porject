#!/bin/bash
sleep 1
ssh pi@$1 <<EOF
rm DataArchiver/* -f
./getCapacity.py /media/pi/ds/
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 1
exit
EOF
scp *.py pi@$1:DataArchiver/
done