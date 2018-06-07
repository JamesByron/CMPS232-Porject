#!/bin/bash
current=2
while [ $current -le 4 ]; do
scp *.py pi@192.168.0.$current:DataArchiver/
let current=$current+1
done