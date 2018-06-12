#!/bin/bash
cd data
rm receive_log_combined
rm verify_log_combined
rm FileNames_combined
head -n 1 receive_log_2 > receive_log_combined
head -n 1 verify_log_2 > verify_log_combined
echo -e Destination_file_name\\tChecksum\\tSize\\tPriority\\tNode >> FileNames_combined
sed -e 's/$/\t1/' receive_log_2 | grep -v Got_connection_time >> receive_log_combined
sed -e 's/$/\t1/' verify_log_2 | grep -v Start_verifying >> verify_log_combined
sed -e 's/$/\t1/' FileNames_2 >> FileNames_combined
sed -e 's/$/\t2/' receive_log_3 | grep -v Got_connection_time >> receive_log_combined
sed -e 's/$/\t2/' verify_log_3 | grep -v Start_verifying >> verify_log_combined
sed -e 's/$/\t2/' FileNames_3 >> FileNames_combined
sed -e 's/$/\t3/' receive_log_4 | grep -v Got_connection_time >> receive_log_combined
sed -e 's/$/\t3/' verify_log_4 | grep -v Start_verifying >> verify_log_combined
sed -e 's/$/\t3/' FileNames_4 >> FileNames_combined
cd ..