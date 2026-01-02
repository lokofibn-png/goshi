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
    "ethical_note": "Abide by each source's ToS. Aggressive queries can get your IP banned.",
    "setup_note": "Marketplace modules: 'marketplace search' then 'marketplace install <module>'"
}

def run(env, tools, log_action, launch_tool):
    """Launch recon-ng with workspace selection."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}RECON-NG – OSINT Framework{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    # Check if installed
    if not os.path.exists("/opt/recon-ng/recon-ng"):
        print(f"{C['r']}[!] recon-ng not found. Installing...{C['x']}")
        for cmd in TOOL["source"]:
            subprocess.run(cmd, shell=True)
        log_action("INSTALL", "recon-ng")

    workspace = input(f"{C['g']}[?] Workspace name [default]: {C['x']}").strip() or "default"
    
    print(f"\n{C['m']}[*] Launching recon-ng in workspace '{workspace}'...{C['x']}")
    log_action("LAUNCH", "recon-ng")
    
    try:
        subprocess.run(f"cd /opt/recon-ng && python3 recon-ng -w {workspace}", shell=True)
        log_action("COMPLETE", f"recon-ng_workspace_{workspace}")
    except Exception as e:
        log_action("ERROR", f"recon-ng_failed_{str(e)}")

    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

if __name__ == "__main__":
    from os_detector import detect_environment
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    run(env, {}, log, lambda c, e: print(f"Launch: {c['name']}"))
