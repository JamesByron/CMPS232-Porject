#!/bin/bash
ssh pi@$1 -tt <<EOF
cd DataArchiver
touch FileNames
nohup python3 receiveFile.py FileNames &
exit
EOF