#!/bin/bash
current=2
while [ $current -le 4 ]; do
ssh pi@192.168.0.$current <<EOF
rm DataArchiver/* -f
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 10
exit
EOF
scp *.py pi@192.168.0.$current:DataArchiver/
let current=$current+1
done