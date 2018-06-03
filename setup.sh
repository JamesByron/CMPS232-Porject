#!/bin/bash
current=2
while [ $current -le 4 ]; do
ssh pi@192.168.0.$current <<EOF
rm DataArchiver/* -f
sudo killall hd-idle
sudo umount /dev/sda1
echo Starting new setup... >> log-hd-idle
sudo hd-idle/hd-idle -i 10 -d >> log-hd-idle
exit
EOF
scp *.py pi@192.168.0.$current:DataArchiver/
ssh pi@192.168.0.$current <<EOF
cd DataArchiver
python3 receiveFile.py &
exit
EOF
let current=$current+1
done