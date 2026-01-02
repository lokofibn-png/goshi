#!/usr/bin/env python3
"""
RECON-NG – Web Reconnaissance Framework
Automated OSINT harvesting from 50+ data sources.
"""

TOOL = {
    "name": "recon-ng",
    "description": "OSINT web reconnaissance framework – Automated data harvesting from 50+ sources",
    "category": "reconnaissance",
    "source": ["git clone https://github.com/lanmaster53/recon-ng.git /opt/recon-ng"],
    "launch_cmd": "python3 /opt/recon-ng/recon-ng",
    "ethical_note": "Abide by each source's ToS. Aggressive queries can get your IP banned."
}

def run(env, tools, log_action, launch_tool):
    """Launch recon-ng with workspace selection."""
    workspace = input(f"\033[1;32m[?] Workspace name [default]: \033[0m").strip() or "default"
    print(f"\033[1;34m[*] Launching recon-ng in workspace '{workspace}'...{C['x']}")
    log_action("LAUNCH", "recon-ng")
    subprocess.run(f"cd /opt/recon-ng && python3 recon-ng -w {workspace}", shell=True)
