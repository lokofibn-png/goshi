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
    "ethical_note": "Only brute-force sites you own. Use '-t 5' to rate-limit and avoid DoS.",
    "rate_limit": True
}

def run(env, tools, log_action, launch_tool):
    """Interactive Gobuster launcher with rate limiting."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}GOBUSTER – Directory Brute-Forcer{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    url = input(f"{C['g']}[?] Target URL (http://example.com): {C['x']}").strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    
    wordlist = input(f"{C['g']}[?] Wordlist path [/usr/share/wordlists/common.txt]: {C['x']}").strip() or "/usr/share/wordlists/common.txt"
    threads = input(f"{C['g']}[?] Threads (rate limit) [5]: {C['x']}").strip() or "5"
    extensions = input(f"{C['g']}[?] File extensions (e.g., php,txt,js) [optional]: {C['x']}").strip()
    
    print(f"\n{C['m']}[*] Brute-forcing {url}...{C['x']}")
    log_action("LAUNCH", "gobuster")
    
    cmd = f"gobuster dir -u {url} -w {wordlist} -t {threads}"
    if extensions:
        cmd += f" -x {extensions}"
    
    try:
        subprocess.run(cmd, shell=True)
        log_action("COMPLETE", f"gobuster_scan_{url.replace('http://', '').replace('https://', '')}")
    except Exception as e:
        log_action("ERROR", f"gobuster_failed_{str(e)}")

    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

if __name__ == "__main__":
    from os_detector import detect_environment
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    run(env, {}, log, lambda c, e: print(f"Launch: {c['name']}"))
