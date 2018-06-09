#!/bin/bash
ssh pi@$1 -tt <<EOF
sudo killall python3
sudo killall hd-idle
sudo umount /dev/sda1
sudo mount /dev/sda1 /media/pi/
rm /media/pi/* -Rf
sudo umount /dev/sda1
rm ~/DataArchiver/*
exit
EOF
rm receive_log_master