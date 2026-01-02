GOSHI – Ghost Protocol Arsenal

A cross-platform ethical hacking toolkit that detects your environment and builds the arsenal you need.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-lightgrey)

---

What is GOSHI?

GOSHI is a modular, self-configuring penetration testing framework that automatically detects whether you're running on Termux (Android) or Linux and installs the appropriate tools. It provides:

- Automated tool installation for 30+ common security tools
- Custom attack vector demos (DDoS, SQLi, packet crafting, hash cracking)
- Integrated update system (git pull + pip upgrade + tool rebuild)
- Audit trail logging for ethical transparency
- Interactive help system to learn what each tool does

> ⚠️ ETHICAL USE ONLY – This toolkit is designed for authorized security testing, bug bounty programs, and educational purposes. All actions are logged to `logs/audit.log`.

---

Quick Start

```bash
# Clone the repository
git clone https://github.com/lokofibn-png/goshi.git
cd goshi

# Run the main protocol
python main.py
```

---

Platform-Specific Installation

📱 Termux (Android)

```bash
# Update Termux packages
pkg update && pkg upgrade -y

# Install required dependencies
pkg install -y python git curl wget

# Clone and enter
git clone https://github.com/lokofibn-png/goshi.git
cd goshi

# Start the ghost protocol
python main.py
```

🐧 Linux (Debian/Ubuntu/Kali)

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and git
sudo apt install -y python3 python3-pip git

# Clone and enter
git clone https://github.com/lokofibn-png/goshi.git
cd goshi

# Start the ghost protocol
python3 main.py
```

🐧 Linux (Arch)

```bash
# Update system
sudo pacman -Syu --noconfirm

# Install dependencies
sudo pacman -S --noconfirm python python-pip git

# Clone and run
git clone https://github.com/lokofibn-png/goshi.git
cd goshi
python main.py
```

🐧 Linux (Fedora/CentOS)

```bash
# Update system
sudo dnf upgrade -y

# Install dependencies
sudo dnf install -y python3 python3-pip git

# Clone and run
git clone https://github.com/lokofibn-png/goshi.git
cd goshi
python3 main.py
```

---

Usage

Main Menu

Run `python main.py` to see:

```
                  .o88o.
                  888 `"
                 o888oo   .oooo.o  .ooooo.   .ooooo.
[ENVIRONMENT: Kali Linux | PKG: apt]
Privacy is a myth—choose your weapon
[MAIN MENU]
==================================================
1.  Reconnaissance & Information Gathering
2.  Vulnerability Assessment
3.  Exploitation Frameworks
4.  Post-Exploitation & Persistence
5.  Password Attacks
6.  Wireless Attacks
7.  Web Application Testing
8.  Network Analysis
9.  Social Engineering
10. Custom Attack Vectors (Ethical Testing Only)
11. Install/Update All Tools
12. Audit Trail
13. Update / Refresh Arsenal (git pull + pip upgrade + tool rebuild)
0.  Exit to Void
==================================================
```

Install All Tools

Select `11` → type `HELL YES` to install every tool in the manifest.

Update Arsenal

Select `13` to:
- Pull latest code from GitHub
- Upgrade all Python packages
- Rebuild tools flagged for auto-update
- Optionally upgrade system packages

View Audit Trail

Select `12` to see all logged actions (timestamp, command, user, PID).

Help System

A standalone help utility explains every tool:

```bash
python help.py
```

Type a number to see a detailed description of any tool or action.

---

Tool Arsenal

Reconnaissance & Information Gathering
- nmap – Network scanner & mapper
- maltego – Link analysis & OSINT
- shodan – IoT search engine CLI
- recon-ng – OSINT web reconnaissance framework
- gobuster – Directory/file brute-forcer
- dirb – Web content scanner

Vulnerability Assessment
- sqlmap – SQL injection automation
- nikto – Web server scanner
- openvas – Vulnerability scanner
- zap – OWASP Zed Attack Proxy

Exploitation Frameworks
- metasploit – Penetration testing framework
- beef – Browser Exploitation Framework
- empire – Post-exploitation framework

Post-Exploitation & Persistence
- mimikatz – Windows credential extraction
- bloodhound – Active Directory path analysis
- responder – LLMNR/NBT-NS poisoning

Password Attacks
- hydra – Login brute-forcer
- john – Password cracker
- hashcat – Advanced hash cracking

Wireless Attacks
- aircrack-ng – WiFi security auditing
- kismet – Wireless network detector

Network Analysis
- wireshark – Protocol analyzer
- ettercap – Man-in-the-middle toolkit
- netcat – Swiss army knife of networking

Social Engineering
- setoolkit – Social-Engineer Toolkit
- maltego – OSINT & link analysis

Custom Attack Vectors
- Spectral DDoS Simulator – Localhost stress testing demo
- SQL Wraith – SQLi demo + vulnerable webapp
- Packet Phantom – ICMP/UDP/TCP packet crafting
- Hash Ritual – Automated hash cracking orchestrator

---

File Structure

```
goshi/
├── main.py                 # Main menu & orchestrator
├── update.py               # Standalone update script
├── help.py                 # Interactive help system
├── os_detector.py          # OS & package manager detection
├── installer.py            # Tool installation engine
├── launchers.py            # Tool execution wrappers
├── config/
│   └── tool_manifest.json  # Tool definitions & dependencies
├── custom_tools/
│   ├── spectral_ddos.py    # DDoS testing framework
│   ├── sql_wraith.py       # SQLi demonstration toolkit
│   ├── packet_phantom.py   # Packet crafting utility
│   └── hash_ritual.py      # Hash cracking orchestrator
├── logs/
│   └── audit.log           # Ethical usage audit trail
└── README.md               # This file
```

---

Ethical Usage Covenant

By using GOSHI, you solemnly attest that:

1. You have explicit written permission for all targets you test
2. You operate within legal bug bounty programs or internal security audits
3. All DDoS/stress testing is confined to your own infrastructure
4. You will never use these tools for illegal, malicious, or unauthorized purposes
5. All actions are logged to `logs/audit.log` for legal transparency

"We who test the locks must never become the thieves."

Violation of these terms violates the CFAA, EU Cybercrime Directive, and your own conscience.

---

Troubleshooting

KeyError: 'package_manager'
→ Fixed in latest commit. Pull updates: `python update.py`

ModuleNotFoundError: No module named 'launchers'
→ Ensure `launchers.py` exists in the same directory

Permission denied on Termux
→ Run `termux-setup-storage` and grant storage permissions

---

Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-tool`)
3. Add your tool to `config/tool_manifest.json`
4. Test on both Termux and Linux
5. Commit with clear messages
6. Open a pull request

---

License

GNU General Public License v3.0 – see [LICENSE](LICENSE) for details.

---

Disclaimer

This tool is provided as-is for educational and authorized testing purposes only. The authors assume no liability for misuse. Use responsibly or not at all.

---

The ghost watches, the ghost remembers, the ghost tests only what it owns.
