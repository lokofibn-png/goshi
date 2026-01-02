#!/usr/bin/env python3
"""
NMAP – Network Mapper
The de facto standard for network discovery and security auditing.
"""

TOOL = {
    "name": "nmap",
    "description": "Network scanner & mapper – Discover hosts, ports, services, OS fingerprints",
    "category": "reconnaissance",
    "dependencies": ["nmap"],
    "launch_cmd": "nmap",
    "ethical_note": "Only scan networks you own or have explicit, written permission to test.",
    "safety_check": lambda target: target in ["127.0.0.1", "localhost", "::1"] or 
        input(f"\n\033[1;31m⚠️  WARNING:\033[0m \033[1;33mYou are about to scan \033[1;37m{target}\033[0m. "
              f"Do you have written authorization? [y/N]: \033[0m").strip().lower() == "y"
}

def run(env, tools, log_action, launch_tool):
    """Interactive Nmap launcher with safety checks."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}NMAP – Network Mapper{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    target = input(f"\n{C['g']}[?] Target IP/hostname: {C['x']}").strip()
    
    # Ethical confirmation
    if not TOOL["safety_check"](target):
        print(f"{C['r']}[!] Action denied: No authorization for target.{C['x']}")
        log_action("DENIED", f"nmap_unauthorized_{target}")
        time.sleep(2)
        return

    # Scan type selection
    print(f"\n{C['y']}Scan Types:{C['x']}")
    print(f"1. Quick scan (-sV -sC -O)")
    print(f"2. Comprehensive scan (-A -p-)")
    print(f"3. Stealth scan (-sS -f)")
    print(f"4. Custom flags")
    
    scan_choice = input(f"{C['g']}[?] Select scan type [1]: {C['x']}").strip() or "1"
    
    flags = {
        "1": "-sV -sC -O",
        "2": "-A -p-",
        "3": "-sS -f",
        "4": input(f"{C['g']}[?] Enter custom nmap flags: {C['x']}").strip()
    }.get(scan_choice, "-sV -sC -O")
    
    # Construct command
    cmd = f"nmap {flags} {target}"
    output_file = input(f"{C['g']}[?] Save output to file (optional): {C['x']}").strip()
    
    if output_file:
        cmd += f" -oN {output_file}"
        print(f"{C['c']}[*] Results will be saved to {output_file}{C['x']}")
    
    print(f"\n{C['m']}[*] Launching nmap against {target}...{C['x']}")
    log_action("LAUNCH", "nmap")
    
    try:
        subprocess.run(cmd, shell=True, check=False)
        log_action("COMPLETE", f"nmap_scan_{target}")
    except Exception as e:
        log_action("ERROR", f"nmap_failed_{str(e)}")

    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

# For standalone execution
if __name__ == "__main__":
    from os_detector import detect_environment
    from launchers import launch_tool
    
    env = detect_environment()
    tools = {}
    log = lambda a, t: print(f"LOG: {a} - {t}")
    
    def dummy_launch(cfg, env):
        print(f"Would launch: {cfg['launch_cmd']}")
    
    run(env, tools, log, dummy_launch)
