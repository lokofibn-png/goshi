#!/usr/bin/env python3
"""
Reconnaissance & Information Gathering Suite
Each tool mapped, explained, and ready for summoning.
"""

TOOLS = {
    "nmap": {
        "name": "nmap",
        "description": "Network scanner & mapper – Discover hosts, ports, services, OS fingerprints",
        "dependencies": ["nmap"],
        "launch_cmd": "nmap"
    },
    "maltego": {
        "name": "maltego",
        "description": "Link analysis & OSINT – Visualize relationships between people, domains, IPs",
        "dependencies": ["maltego"],
        "launch_cmd": "maltego"
    },
    "shodan": {
        "name": "shodan",
        "description": "IoT & device search engine – Query exposed services, vulnerabilities, banners",
        "dependencies": ["python3"],
        "python_packages": ["shodan"],
        "launch_cmd": "shodan"
    },
    "recon-ng": {
        "name": "recon-ng",
        "description": "OSINT web reconnaissance framework – Automated data harvesting from 50+ sources",
        "source": ["git clone https://github.com/lanmaster53/recon-ng.git /opt/recon-ng"],
        "launch_cmd": "python3 /opt/recon-ng/recon-ng"
    },
    "gobuster": {
        "name": "gobuster",
        "description": "Directory/file brute-forcer – Fast web content discovery",
        "dependencies": ["gobuster"],
        "launch_cmd": "gobuster"
    },
    "dirb": {
        "name": "dirb",
        "description": "Web content scanner – Classic directory buster with wordlists",
        "dependencies": ["dirb"],
        "launch_cmd": "dirb"
    }
}


def show_menu(env, tools, log_action, launch_tool):
    """
    Interactive menu for reconnaissance tools.
    Filters TOOLS from master manifest and presents numbered list.
    """
    # Filter only reconnaissance tools from the master tools dict
    category_tools = {k: v for k, v in tools.items() if k in TOOLS}

    while True:
        # Clear screen (Termux-safe)
        os.system("clear" if env["os"] != "termux" else "clear")

        # Header
        print("\033[1;34m")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║  RECONNAISSANCE & INFORMATION GATHERING                    ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print("\033[0m")

        # Tool list
        print("\033[1;33m")
        for idx, (name, cfg) in enumerate(category_tools.items(), 1):
            print(f"{idx:2}. \033[1;36m{name.upper():<12}\033[0m\033[1;33m- {cfg['description']}\033[0m")
        print("\033[1;33m 0. \033[1;31mReturn to Mainframe\033[0m")
        print("\033[1;34m" + "=" * 60 + "\033[0m")

        # Selection
        c = input("\n\033[1;32m[?] Select Tool: \033[0m").strip()

        if c == "0":
            break

        try:
            # Map number to tool name
            tool_name = list(category_tools.keys())[int(c) - 1]
            cfg = category_tools[tool_name]

            # Log and launch
            log_action("LAUNCH", tool_name)
            print(f"\n\033[1;35m[*] Summoning {tool_name}...\033[0m")
            launch_tool(cfg, env)

        except (IndexError, ValueError):
            print("\n\033[1;31m[!] Invalid selection.\033[0m")
            time.sleep(1)
        except Exception as e:
            print(f"\n\033[1;31m[!] Error: {e}\033[0m")
            time.sleep(1)


# If run standalone, demo the menu
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from os_detector import detect_environment
    from launchers import launch_tool

    env = detect_environment()
    tools = TOOLS  # Use local TOOLS dict for demo

    def dummy_log(action, tool):
        print(f"[LOG] {action}: {tool}")

    show_menu(env, tools, dummy_log, launch_tool)
