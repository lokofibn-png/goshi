#!/usr/bin/env python3
"""
SHODAN – The Search Engine for Hackers
IoT & Device Exposure Intelligence
"""

TOOL = {
    "name": "shodan",
    "description": "IoT & device search engine – Query exposed services, vulnerabilities, banners",
    "category": "reconnaissance",
    "dependencies": ["python3"],
    "python_packages": ["shodan"],
    "launch_cmd": "shodan",
    "setup_note": "Run 'shodan init <YOUR_API_KEY>' after installation.",
    "ethical_note": "Never query critical infrastructure (hospitals, power grids) without authorization."
}

def run(env, tools, log_action, launch_tool):
    """Interactive Shodan query interface."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}SHODAN – IoT Search Engine{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    # Check if API key is set
    check_key = subprocess.run("shodan info", shell=True, capture_output=True, text=True)
    if "Invalid API key" in check_key.stderr or check_key.returncode != 0:
        print(f"{C['r']}[!] No valid Shodan API key found.{C['x']}")
        print(f"{C['y']}[*] Get one at: https://account.shodan.io{C['x']}")
        key = input(f"{C['g']}[?] Enter API key: {C['x']}").strip()
        if key:
            subprocess.run(f"shodan init {key}", shell=True)
            log_action("SETUP", "shodan_api_key")
        else:
            return

    query = input(f"\n{C['g']}[?] Shodan query (e.g., 'apache city:Berlin'): {C['x']}").strip()
    if not query:
        return
        
    limit = input(f"{C['g']}[?] Result limit [10]: {C['x']}").strip() or "10"
    output = input(f"{C['g']}[?] Save to file (optional): {C['x']}").strip()
    
    print(f"\n{C['m']}[*] Querying Shodan for: {C['w']}{query}{C['x']}")
    log_action("LAUNCH", "shodan")
    
    cmd = f"shodan search --limit {limit} {query}"
    if output:
        cmd += f" > {output}"
        print(f"{C['c']}[*] Results will be saved to {output}{C['x']}")
    
    try:
        subprocess.run(cmd, shell=True)
        log_action("COMPLETE", f"shodan_query_{query}")
    except Exception as e:
        log_action("ERROR", f"shodan_failed_{str(e)}")

    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

if __name__ == "__main__":
    from os_detector import detect_environment
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    run(env, {}, log, lambda c, e: print(f"Launch: {c['name']}"))
