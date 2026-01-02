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
    query = input(f"\033[1;32m[?] Shodan query (e.g., 'apache city:Berlin'): \033[0m").strip()
    limit = input(f"\033[1;32m[?] Result limit [10]: \033[0m").strip() or "10"
    
    print(f"\033[1;34m[*] Querying Shodan...{C['x']}")
    log_action("LAUNCH", "shodan")
    subprocess.run(f"shodan search --limit {limit} {query}", shell=True)
