#!/usr/bin/env python3
"""
MALTEGO – Link Analysis & OSINT Visualization
Map invisible connections between people, domains, and infrastructure.
"""

TOOL = {
    "name": "maltego",
    "description": "Link analysis & OSINT – Visualize relationships between people, domains, IPs",
    "category": "reconnaissance",
    "dependencies": ["maltego"],
    "launch_cmd": "maltego",
    "ethical_note": "Respect privacy laws. Only map targets you have authorization to investigate."
}

def run(env, tools, log_action, launch_tool):
    """Launch Maltego with a new project prompt."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}MALTEGO – Link Analysis{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    
    project = input(f"{C['g']}[?] Project name (optional): {C['x']}").strip()
    
    print(f"\n{C['m']}[*] Starting Maltego...{C['x']}")
    log_action("LAUNCH", "maltego")
    
    if project:
        # Maltego CLI supports project creation on startup
        subprocess.run(f"maltego --project {project}", shell=True)
    else:
        subprocess.run("maltego", shell=True)

    log_action("COMPLETE", "maltego_session")

if __name__ == "__main__":
    from os_detector import detect_environment
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    run(env, {}, log, lambda c, e: print(f"Launch: {c['name']}"))
