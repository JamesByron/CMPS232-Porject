#!/bin/bash
ssh pi@192.168.0.2 <<'EOF'
sudo shutdown now
EOF
ssh pi@192.168.0.3 <<'EOF2'
sudo shutdown now
EOF2
ssh pi@192.168.0.4 <<'EOF3'
sudo shutdown now
EOF3
