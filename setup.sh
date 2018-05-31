#!/bin/bash
ssh pi@192.168.0.2 <<'EOF'
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 1
exit
EOF
ssh pi@192.168.0.3 <<'EOF'
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 1
exit
EOF
ssh pi@192.168.0.4 <<'EOF'
sudo umount /dev/sda1
sudo hd-idle/hd-idle -i 1
exit
EOF