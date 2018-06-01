#!/bin/bash
current=2
while [ $current -le 4 ]; do
ssh pi@192.168.0.$current <<EOF
sudo shutdown now
EOF
let current=$current+1
done