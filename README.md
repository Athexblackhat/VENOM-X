<div align="center">

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=3000&pause=500&color=F70000&center=true&vCenter=true&width=600&lines=VENOM-X;THE+ULTIMATE+TOOLKIT;5%2C268+TOOLS;CREATED+BY+ATHEX+BLACK+HAT" alt="VENOM-X Typing SVG" />
</p>

<pre style="background: #0a0a0a; color: #ff0000; padding: 20px; border-radius: 10px; font-family: monospace; font-size: 12px;">

    ██╗   ██╗███████╗███╗   ██╗ ██████╗ ███╗   ███╗    ██╗  ██╗            
    ██║   ██║██╔════╝████╗  ██║██╔═══██╗████╗ ████║    ╚██╗██╔╝            
    ██║   ██║█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║     ╚███╔╝             
    ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║     ██╔██╗             
     ╚████╔╝ ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║    ██╔╝ ██╗            
      ╚═══╝  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝    ╚═╝  ╚═╝            

</pre>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-red?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Tools-5%2C268-red?style=for-the-badge&logo=hackthebox" alt="Tools">
  <img src="https://img.shields.io/badge/Python-3.8%2B-red?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-red?style=for-the-badge&logo=linux" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-red?style=for-the-badge&logo=opensource" alt="License">
</p>

</div>

---

## VENOM-X

**VENOM-X** is a professional, animated, all-in-one toolkit manager that gives access to **5,268+ tools** organized across **15+ categories**. It provides a dark terminal UI, animations, and one-click batch installation for security professionals and researchers.

> WARNING: This tool is for EDUCATIONAL PURPOSES ONLY. The developer is NOT responsible for any misuse. Use responsibly and only on systems you own or have explicit permission to test.

---

## FEATURES

- 5,268+ Tools: Large curated database
- 15+ Categories: Organized by tool type
- Multiple Themes: Venom, Matrix, Dark, Neon
- One-Click Install: Batch installation of selected tools
- Smart Search: Search by name, description, or language
- Real-time Progress: Animated installation progress
- Cross-platform: Linux, Termux, macOS

---

## TOOL CATEGORIES

| # | Category | Tools |
|---|----------|-------|
| 1 | Hacking Tools | 1,200+ |
| 2 | Penetration Testing | 800+ |
| 3 | Cybersecurity | 600+ |
| 4 | Reconnaissance | 500+ |
| 5 | OSINT Tools | 400+ |
| 6 | Password Cracking | 350+ |
| 7 | Vulnerability Scanners | 300+ |
| 8 | Exploit Database | 250+ |
| 9 | Web Hacking | 200+ |
| 10 | WiFi Hacking | 150+ |
| 11 | Social Engineering | 100+ |
| 12 | Forensics | 100+ |
| 13 | Mobile Hacking | 80+ |
| 14 | Cloud Security | 70+ |
| 15 | Red Team | 60+ |

---

## THEMES PREVIEW

### VENOM THEME (Default)

```
VENOM - Red & Black Theme
Primary: Red
Secondary: Yellow
Accent: Green
Danger: Magenta
```

### MATRIX THEME

```
MATRIX - Green Theme
Primary: Green
Secondary: Light Green
Accent: White
Danger: Red
```

### DARK THEME

```
DARK - Minimal Theme
Primary: White
Secondary: Gray
Accent: Cyan
Danger: Red
```

### NEON THEME

```
NEON - Cyberpunk Theme
Primary: Magenta
Secondary: Light Magenta
Accent: Cyan
Danger: Red
```

---

## INSTALLATION

### Prerequisites

- Python 3.8 or higher
- pip package manager
- git (for cloning tools)

### One-Click Installation (Linux/Termux)

```bash
git clone https://github.com/Athexblakhat/VENOM-X.git
cd VENOM-X
chmod +x setup.sh
./setup.sh
# or
python3 venom_x.py
```

### Manual Installation

```bash
pip3 install -r requirements.txt
mkdir -p ~/.venomx
mkdir -p ~/venomx-tools
python3 venom_x.py
```

### Termux Installation

```bash
pkg update && pkg upgrade
pkg install python git
pip3 install -r requirements.txt
git clone https://github.com/Athexblakhat/VENOM-X.git
cd VENOM-X
python3 venom_x.py
```

---

## HOW TO USE

Run the program and follow the menu prompts. Typical menu options include:

1. Install Tools
2. Browse Categories
3. Search Tools
4. View Selections
5. Change Theme
6. Settings
7. About
8. Exit

Select a category to view tools, toggle selection by number, and press `i` to install selected tools.

---

## ANIMATIONS

VENOM-X includes several terminal animations used for UX polish:

- Matrix Rain: Startup/Exit animation
- TypeWriter: Banner display
- Spinner: Loading indicators
- Progress Bar: Installation progress
- Glitch: Optional text effect

---

---

## REQUIREMENTS

Install required Python packages:

```bash
pip3 install -r requirements.txt
```

Minimal requirements:

- rich>=13.7.0
- prompt-toolkit>=3.0.0
- pyfiglet>=0.8.post1
- colorama>=0.4.6
- requests>=2.31.0

---

## COMMANDS CHEAT SHEET

| Action | Command |
|--------|---------|
| Install selected tools | 1 |
| Browse categories | 2 |
| Search tools | 3 |
| View selections | 4 |
| Change theme | 5 |
| Settings | 6 |
| About | 7 |
| Exit | 8 |
| Select tool | [number] |
| Install selected | i |
| Clear selections | c |
| Go back | 0 |

---

## CONFIGURATION

User configuration is stored at `config.json`.

Example:

```json
{
  "theme": "venom",
  "install_path": "/home/user/venomx-tools",
  "auto_update": true,
  "animations": true,
  "sound_effects": false,
  "last_updated": 1716789123.456,
  "installed_tools": ["nmap", "metasploit", "wireshark"],
  "selected_tools": ["nmap", "wireshark"]
}
```

---

## UPDATING

To update the project and dependencies:

```bash
git pull
pip3 install --upgrade -r requirements.txt
python3 venom_x.py
```

---

## TROUBLESHOOTING

Common issues and fixes:

- `ModuleNotFoundError`: Run `pip3 install -r requirements.txt`
- JSON file not found: Ensure `hacking_tools_ultimate.json` is in the repository
- Permission denied: Run with appropriate privileges or adjust file permissions
- Tools not installing: Verify internet connection and `git` availability
- Theme not applying: Remove `~/.venomx/theme.json` and restart

---

## LICENSE

MIT License

Copyright (c) 2026 ATHEX BLACK HAT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text omitted for brevity in README]

---

## DISCLAIMER

This tool is for educational purposes only. Use responsibly and only on systems you own or are authorized to test.

---

## CONTACT

Platform | Handle
---|---
GitHub | @Athexblackhat
TikTok | @team.athex1


---

## SUPPORT

If you find VENOM-X useful, consider:

- Starring the repository
- Forking the project
- Following for updates
- Contributing to development
