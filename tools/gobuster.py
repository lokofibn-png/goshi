#!/usr/bin/env python3
"""
GOBUSTER – Fast Directory/File Brute-Forcer
Blazing-speed web content discovery.
"""

TOOL = {
    "name": "gobuster",
    "description": "Directory/file brute-forcer – Fast web content discovery",
    "category": "reconnaissance",
    "dependencies": ["gobuster"],
    "launch_cmd": "gobuster",
    "ethical_note": "Only brute-force sites you own. Use '-t 5' to rate-limit and avoid DoS."
}

def run(env, tools, log_action, launch_tool):
    """Interactive Gobuster launcher."""
    url = input(f"\033[1;32m[?] Target URL (http://example.com): \033[0m").strip()
    wordlist = input(f"\033[1;32m[?] Wordlist path [/usr/share/wordlists/common.txt]: \033[0m").strip() or "/usr/share/wordlists/common.txt"
    threads = input(f"\033[1;32m[?] Threads (rate limit) [5]: \033[0m").strip() or "5"
    
    print(f"\033[1;34m[*] Brute-forcing {url}...{C['x']}")
    log_action("LAUNCH", "gobuster")
    subprocess.run(f"gobuster dir -u {url} -w {wordlist} -t {threads}", shell=True)
