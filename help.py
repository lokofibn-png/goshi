#!/usr/bin/env python3
import os
import json
import sys

# ANSI colors
C = {
    "r": "\033[1;31m",  # red
    "g": "\033[1;32m",  # green
    "y": "\033[1;33m",  # yellow
    "b": "\033[1;34m",  # blue
    "m": "\033[1;35m",  # magenta
    "c": "\033[1;36m",  # cyan
    "w": "\033[1;37m",  # white
    "x": "\033[0m"      # reset
}

def load_manifest():
    with open("config/tool_manifest.json", "r") as f:
        return json.load(f)

def build_help_index(tools):
    """Combine tools + menu actions into a single numbered index."""
    index = []

    # Core tools from manifest
    for num, (name, cfg) in enumerate(tools.items(), 1):
        desc = cfg.get("description", "No description")
        index.append((num, name.upper(), desc))

    # Main menu actions (add after tools)
    menu_start = len(index) + 1
    menu_items = [
        ("INSTALL/UPDATE", "Install or update every tool in the arsenal"),
        ("AUDIT TRAIL", "View a log of all actions taken (ethical paper trail)"),
        ("UPDATE ARSENAL", "Git pull, pip upgrade, and rebuild tools"),
        ("EXIT", "Return to the void")
    ]
    for num, (label, desc) in enumerate(menu_items, menu_start):
        index.append((num, label, desc))

    return index

def show_help():
    tools = load_manifest()
    help_index = build_help_index(tools)

    while True:
        os.system("clear" if os.path.exists("/data/data/com.termux") else "clear")
        print(f"{C['g']}\n╔════════════════════════════════════════════════════════════╗{C['x']}")
        print(f"{C['g']}║  THE GHOST PROTOCOL - INDEX OF TOOLS & ACTIONS             ║{C['x']}")
        print(f"{C['g']}╚════════════════════════════════════════════════════════════╝{C['x']}\n")

        # Print numbered list
        for num, name, desc in help_index:
            print(f"{C['y']}[{num:2}]{C['x']} {C['c']}{name:<25}{C['x']} - {desc}")

        print(f"\n{C['m']}Type a number to see details, or 0 to return{C['x']}")
        choice = input(f"{C['y']}>> {C['x']}").strip()

        if choice == "0":
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(help_index):
                _, name, desc = help_index[choice - 1]
                print(f"\n{C['g']}═══════════════════════════════════════════════════════════{C['x']}")
                print(f"{C['c']}{name}{C['x']}")
                print(f"{C['g']}═══════════════════════════════════════════════════════════{C['x']}")
                print(f"{desc}\n")
                input("Press Enter to continue...")
            else:
                print(f"{C['r']}Invalid number.{C['x']}")
                time.sleep(1)
        except ValueError:
            print(f"{C['r']}Type a number or 0.{C['x']}")
            time.sleep(1)


if __name__ == "__main__":
    show_help()
