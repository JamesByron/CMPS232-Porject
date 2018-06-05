#!/bin/bash
current=2
scp *.py pi@192.168.0.$current:DataArchiver/
while [ $current -le 2 ]; do
ssh pi@192.168.0.$current <<EOF
cd DataArchiver
python3 receiveFile.py &
exit
EOF
let current=$current+1
done