#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${RED}"
cat << "EOF"

██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗     ██╗  ██╗
██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║     ╚██╗██╔╝
██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║█████╗╚███╔╝ 
╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║╚════╝██╔██╗ 
 ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║     ██╔╝ ██╗
  ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝     ╚═╝  ╚═╝
                                                            
                  VENOM-X INSTALLER                         
             Created by ATHEX BLACK HAT

EOF
echo -e "${NC}"

sleep 2

echo -e "${YELLOW}[+] Checking system...${NC}"
sleep 1

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}[OK] Python3 found${NC}"
else
    echo -e "${RED}[FAIL] Python3 not found! Installing...${NC}"
    pkg install python -y 2>/dev/null || apt install python3 -y
fi

if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[OK] pip3 found${NC}"
else
    echo -e "${YELLOW}[WARN] pip3 not found, installing...${NC}"
    python3 -m ensurepip --upgrade
fi

echo -e "${YELLOW}[+] Installing Python dependencies...${NC}"
pip3 install rich prompt-toolkit pyfiglet colorama requests --quiet

echo -e "${YELLOW}[+] Creating directory structure...${NC}"
mkdir -p ~/.venomx
mkdir -p ~/venomx-tools

echo -e "${YELLOW}[+] Downloading VENOM-X...${NC}"
cat > ~/venom-x.py << 'EOF'
EOF

chmod +x ~/venom-x.py

echo -e "${GREEN}"
cat << "EOF"                                                        
         VENOM-X INSTALLED SUCCESSFULLY!
                                                        
     Run: python3 ~/venom_x.py
                                                        
     Created by ATHEX BLACK HAT
EOF
echo -e "${NC}"

read -p "Run VENOM-X now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 ~/venom_x.py
fi
