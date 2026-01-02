#!/usr/bin/env python3
"""
DIRB – Web Content Scanner
Classic directory buster with recursive capability.
"""

TOOL = {
    "name": "dirb",
    "description": "Web content scanner – Classic directory buster with wordlists",
    "category": "reconnaissance",
    "dependencies": ["dirb"],
    "launch_cmd": "dirb",
    "ethical_note": "Respect robots.txt. Default wordlist is aggressive; use -r for recursion."
}

def run(env, tools, log_action, launch_tool):
    """Simple DIRB launcher."""
    url = input(f"\033[1;32m[?] Target URL: \033[0m").strip()
    print(f"\033[1;34m[*] Scanning {url}...{C['x']}")
    log_action("LAUNCH", "dirb")
    subprocess.run(f"dirb {url}", shell=True)
