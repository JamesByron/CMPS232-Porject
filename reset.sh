#!/bin/bash
current=2
while [ $current -le 4 ]; do
ssh pi@192.168.0.$current -tt <<EOF
rm DataArchiver/* -f
rm /media/pi/ds/* -Rf
exit
EOF
let current=$current+1
done