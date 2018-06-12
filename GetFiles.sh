#!/bin/bash
current=2
cd data
while [ $current -le 4 ]; do
	scp pi@192.168.0.$current:DataArchiver/receive_log receive_log_$current
	scp pi@192.168.0.$current:DataArchiver/verify_log verify_log_$current
	scp pi@192.168.0.$current:DataArchiver/FileNames FileNames_$current
let current=$current+1
done
cd ..