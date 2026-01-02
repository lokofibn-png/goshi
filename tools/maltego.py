#!/usr/bin/env python3
"""
MALTEGO – Link Analysis & OSINT Visualization
Map the invisible connections between people, domains, and infrastructure.
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
    print(f"\033[1;34m[*] Starting Maltego...{C['x']}")
    log_action("LAUNCH", "maltego")
    subprocess.run("maltego", shell=True)
