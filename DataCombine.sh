#!/bin/bash
cd data
rm receive_log_combined.tsv
rm verify_log_combined.tsv
rm FileNames_combined.tsv
head -n 1 receive_log_2 > receive_log_combined.tsv
head -n 1 verify_log_2 > verify_log_combined.tsv
echo -e Destination_file_name\\tChecksum\\tSize\\tPriority\\tNode >> FileNames_combined.tsv
sed -e 's/$/\t1/' receive_log_2 | grep -v Got_connection_time >> receive_log_combined.tsv
sed -e 's/$/\t1/' verify_log_2 | grep -v Start_verifying >> verify_log_combined.tsv
sed -e 's/$/\t1/' FileNames_2 | tr -s " " | tr " " "\t" >> FileNames_combined.tsv
sed -e 's/$/\t2/' receive_log_3 | grep -v Got_connection_time >> receive_log_combined.tsv
sed -e 's/$/\t2/' verify_log_3 | grep -v Start_verifying >> verify_log_combined.tsv
sed -e 's/$/\t2/' FileNames_3 | tr -s " " | tr " " "\t" >> FileNames_combined.tsv
sed -e 's/$/\t3/' receive_log_4 | grep -v Got_connection_time >> receive_log_combined.tsv
sed -e 's/$/\t3/' verify_log_4 | grep -v Start_verifying >> verify_log_combined.tsv
sed -e 's/$/\t3/' FileNames_4 | tr -s " " | tr " " "\t" >> FileNames_combined.tsv
rm speed.tsv
rm busyness.tsv
rm verify.tsv
cd ..
python3 DataProcessing.py
./charts.sh
cd paper
make clean
make
cd ..