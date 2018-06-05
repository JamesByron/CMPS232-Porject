#!/bin/bash
current=2
while [ $current -le 4 ]; do
scp *.py pi@192.168.0.$current:DataArchiver/
ssh pi@192.168.0.$current -tt <<EOF
cd DataArchiver
echo Starting_new_log >> ~/receive_log
python3 receiveFile.py & >> ~/receive_log
exit
EOF
let current=$current+1
done