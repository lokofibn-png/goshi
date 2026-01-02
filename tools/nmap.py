#!/usr/bin/env python3
"""
NMAP – Network Mapper
De Facto Standard for Network Discovery & Security Auditing
"""

TOOL = {
    "name": "nmap",
    "description": "Network scanner & mapper – Discover hosts, ports, services, OS fingerprints",
    "category": "reconnaissance",
    "dependencies": ["nmap"],
    "launch_cmd": "nmap",
    "ethical_note": "Only scan networks you own or have explicit, written permission to test.",
    "safety_check": lambda target: target in ["127.0.0.1", "localhost", "::1"] or 
        input(f"\033[1;31m⚠️  WARNING:\033[0m \033[1;33mYou are about to scan \033[1;37m{target}\033[0m. "
              f"Do you have written authorization? [y/N]: \033[0m").strip().lower() == "y"
}

def run(env, tools, log_action, launch_tool):
    """Interactive Nmap launcher with safety checks."""
    import subprocess
    
    target = input(f"\033[1;32m[?] Target IP/hostname: \033[0m").strip()
    if not TOOL["safety_check"](target):
        print(f"\033[1;31m[!] Action denied: No authorization for target.{C['x']}")
        log_action("DENIED", "nmap_unauthorized_target")
        return

    print(f"\033[1;34m[*] Launching nmap against {target}...\033[0m")
    cmd = f"nmap -sV -sC -O {target}"  # Service version, default scripts, OS detection
    log_action("LAUNCH", "nmap")
    subprocess.run(cmd, shell=True)
