#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  RECONNAISSANCE & INFORMATION GATHERING SUITE                            ║
║  Ethical OSINT & Network Discovery Framework                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

This module provides automated, logged, and safety-guarded wrappers for
industry-standard reconnaissance tools. Every action is audited, every
target must be explicitly authorized.

⚠️  ETHICAL MANDATE: You must have written permission for every target.
"""

import os
import sys
import time
import subprocess
from typing import Dict, Any, Callable, List

# ANSI Colors for terminal output
C = {
    "r": "\033[1;31m",  # red - errors
    "g": "\033[1;32m",  # green - success
    "y": "\033[1;33m",  # yellow - warnings
    "b": "\033[1;34m",  # blue - headers
    "m": "\033[1;35m",  # magenta - actions
    "c": "\033[1;36m",  # cyan - info
    "w": "\033[1;37m",  # white - bright text
    "d": "\033[0;90m",  # dim - metadata
    "x": "\033[0m"      # reset
}

# ──────────────────────────────────────────────────────────────────────────
# TOOL ARSENAL - Detailed configuration with ethical safeguards
TOOLS: Dict[str, Dict[str, Any]] = {
    "nmap": {
        "name": "nmap",
        "description": "Network scanner & mapper – Discover hosts, ports, services, OS fingerprints",
        "category": "network",
        "dependencies": ["nmap"],
        "launch_cmd": "nmap",
        "ethical_note": "Only scan networks you own or have explicit permission to test.",
        "safety_check": lambda target: target in ["127.0.0.1", "localhost", "::1"] or input(
            f"{C['r']}⚠️  WARNING: {C['x']}{C['y']}You are about to scan {C['w']}{target}{C['x']}. "
            f"Do you have written authorization? [y/N]: {C['x']}"
        ).strip().lower() == "y"
    },
    "maltego": {
        "name": "maltego",
        "description": "Link analysis & OSINT – Visualize relationships between people, domains, IPs",
        "category": "osint",
        "dependencies": ["maltego"],
        "launch_cmd": "maltego",
        "ethical_note": "Respect privacy laws. Only query public data for authorized targets."
    },
    "shodan": {
        "name": "shodan",
        "description": "IoT & device search engine – Query exposed services, vulnerabilities, banners",
        "category": "osint",
        "dependencies": ["python3"],
        "python_packages": ["shodan"],
        "launch_cmd": "shodan",
        "setup_note": "Run 'shodan init <API_KEY>' after installation.",
        "ethical_note": "Never query critical infrastructure without authorization."
    },
    "recon-ng": {
        "name": "recon-ng",
        "description": "OSINT web reconnaissance framework – Automated data harvesting from 50+ sources",
        "category": "osint",
        "source": ["git clone https://github.com/lanmaster53/recon-ng.git /opt/recon-ng"],
        "launch_cmd": "python3 /opt/recon-ng/recon-ng",
        "ethical_note": "Abide by each source's ToS. Aggressive queries can get you banned."
    },
    "gobuster": {
        "name": "gobuster",
        "description": "Directory/file brute-forcer – Fast web content discovery",
        "category": "web",
        "dependencies": ["gobuster"],
        "launch_cmd": "gobuster",
        "ethical_note": "Only brute-force sites you own. Use rate limiting to avoid DoS."
    },
    "dirb": {
        "name": "dirb",
        "description": "Web content scanner – Classic directory buster with wordlists",
        "category": "web",
        "dependencies": ["dirb"],
        "launch_cmd": "dirb",
        "ethical_note": "Respect robots.txt. Aggressive scanning can be seen as an attack."
    }
}

# ──────────────────────────────────────────────────────────────────────────
def show_menu(env: Dict[str, Any], tools: Dict[str, Any],
              log_action: Callable, launch_tool: Callable):
    """
    Interactive menu for reconnaissance tools with ethical confirmation.
    
    Args:
        env: Environment dict from os_detector
        tools: Master tools manifest
        log_action: Callback to audit log
        launch_tool: Callback to launch a tool
    """
    import os  # Local import for standalone safety
    
    # Filter only reconnaissance tools from master manifest
    category_tools = {k: v for k, v in tools.items() if k in TOOLS}
    
    if not category_tools:
        print(f"{C['r']}No reconnaissance tools available in manifest.{C['x']}")
        input("Press Enter to continue...")
        return

    while True:
        # Clear screen (Termux-safe)
        os.system("clear" if env["os"] != "termux" else "clear")

        # Header with warning banner
        print(f"{C['b']}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║  RECONNAISSANCE & INFORMATION GATHERING                        ║")
        print("║  ⚠️  ETHICAL USE ONLY - AUTHORIZED TARGETS ONLY               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C['x']}")

        # Tool list with numbers
        print(f"{C['y']}")
        for idx, (name, cfg) in enumerate(category_tools.items(), 1):
            print(f"{idx:2d}. {C['c']}{name.upper():<12}{C['x']}{C['y']} - {cfg['description'][:50]}...{C['x']}")
        print(f" 0. {C['r']}Return to Mainframe{C['x']}")
        print(f"{C['b']}{'=' * 64}{C['x']}")

        # Selection
        c = input(f"\n{C['g']}[?] Select Tool: {C['x']}").strip()

        if c == "0":
            log_action("EXIT", "reconnaissance_menu")
            break

        try:
            # Validate selection
            tool_name = list(category_tools.keys())[int(c) - 1]
            cfg = category_tools[tool_name]
            
            # Ethical confirmation if safety_check exists
            if "safety_check" in TOOLS.get(tool_name, {}):
                target = input(f"{C['m']}[?] Target (IP/hostname): {C['x']}").strip()
                if not TOOLS[tool_name]["safety_check"](target):
                    log_action("DENIED", f"{tool_name}_unauthorized_target")
                    print(f"{C['r']}Action denied: No authorization for target.{C['x']}")
                    time.sleep(2)
                    continue

            # Log and launch
            log_action("LAUNCH", tool_name)
            print(f"\n{C['m']}[*] Summoning {tool_name}...{C['x']}")
            launch_tool(cfg, env)

        except (IndexError, ValueError):
            print(f"{C['r']}Invalid selection.{C['x']}")
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{C['y']}Interrupted by user.{C['x']}")
            log_action("INTERRUPT", "reconnaissance_menu")
            break
        except Exception as e:
            print(f"{C['r']}Error: {e}{C['x']}")
            log_action("ERROR", f"reconnaissance_menu_{str(e)}")
            time.sleep(1)


# ──────────────────────────────────────────────────────────────────────────
def show_tool_details(tool_name: str):
    """Display detailed information about a specific tool."""
    if tool_name not in TOOLS:
        print(f"{C['r']}Tool '{tool_name}' not found.{C['x']}")
        return

    cfg = TOOLS[tool_name]
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}{cfg['name'].upper()}{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['y']}Description:{C['x']} {cfg['description']}")
    print(f"{C['y']}Category:{C['x']} {cfg.get('category', 'unknown')}")
    print(f"{C['y']}Dependencies:{C['x']} {', '.join(cfg.get('dependencies', []))}")
    if 'python_packages' in cfg:
        print(f"{C['y']}Python Packages:{C['x']} {', '.join(cfg['python_packages'])}")
    if 'ethical_note' in cfg:
        print(f"{C['r']}⚠️  Ethical Note:{C['x']} {cfg['ethical_note']}")
    if 'setup_note' in cfg:
        print(f"{C['c']}💡 Setup Note:{C['x']} {cfg['setup_note']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}\n")


# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Standalone execution for testing
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from os_detector import detect_environment
    from launchers import launch_tool
    
    env = detect_environment()
    
    # Load merged tools from installer.py pattern
    def get_merged_tools():
        tools = {}
        import glob
        for path in glob.glob("tools/*.py"):
            if path.endswith("__init__.py"): continue
            module = __import__(path[:-3].replace("/", "."), fromlist=["TOOLS"])
            if hasattr(module, "TOOLS"): tools.update(module.TOOLS)
        if os.path.exists("config/tool_manifest.json"):
            import json
            with open("config/tool_manifest.json") as f:
                tools.update(json.load(f))
        return tools
    
    tools = get_merged_tools()
    
    def dummy_log(action, tool):
        print(f"{C['d']}[LOG] {action}: {tool}{C['x']}")
    
    # If tool name provided as arg, show details
    if len(sys.argv) > 1:
        show_tool_details(sys.argv[1])
    else:
        # Otherwise run the menu
        show_menu(env, tools, dummy_log, launch_tool)
