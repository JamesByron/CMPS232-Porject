#!/bin/bash
current=2
while [ $current -le 2 ]; do
ssh pi@192.168.0.$current <<EOF
rm DataArchiver/* -f
sudo killall hd-idle
sudo killall python3
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 10
exit
EOF
let current=$current+1
done