#!/bin/bash
ssh pi@$1 -tt <<EOF
sudo reboot now
EOF