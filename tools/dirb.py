#!/usr/bin/env python3
"""
DIRB – Web Content Scanner
Classic directory buster with wordlists.
"""

TOOL = {
    "name": "dirb",
    "description": "Web content scanner – Classic directory buster with wordlists",
    "category": "reconnaissance",
    "dependencies": ["dirb"],
    "launch_cmd": "dirb",
    "ethical_note": "Respect robots.txt. Default wordlist is aggressive; use -r for recursion.",
    "respect_robots": True
}

def run(env, tools, log_action, launch_tool):
    """Simple DIRB launcher with options."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}DIRB – Web Content Scanner{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    url = input(f"{C['g']}[?] Target URL: {C['x']}").strip()
    wordlist = input(f"{C['g']}[?] Wordlist [/usr/share/wordlists/dirb/common.txt]: {C['x']}").strip() or "/usr/share/wordlists/dirb/common.txt"
    recursive = input(f"{C['g']}[?] Recursive scan? [y/N]: {C['x']}").strip().lower() == "y"
    
    print(f"\n{C['m']}[*] Scanning {url}...{C['x']}")
    log_action("LAUNCH", "dirb")
    
    cmd = f"dirb {url} {wordlist}"
    if recursive:
        cmd += " -r"
    
    try:
        subprocess.run(cmd, shell=True)
        log_action("COMPLETE", f"dirb_scan_{url}")
    except Exception as e:
        log_action("ERROR", f"dirb_failed_{str(e)}")

    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

if __name__ == "__main__":
    from os_detector import detect_environment
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    run(env, {}, log, lambda c, e: print(f"Launch: {c['name']}"))
