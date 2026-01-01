#!/usr/bin/env python3
import subprocess
import os
import shlex

def launch_tool(tool_config, env):
    """
    Ethically launch a tool with user confirmation and logging.
    """
    cmd = tool_config.get("launch_cmd")
    if not cmd:
        print("\033[1;31m[!] No launch command defined for this tool.\033[0m")
        return

    print(f"\n\033[1;33m[*] Launching: {tool_config['name']}\033[0m")
    print(f"    Command: {cmd}")
    confirm = input("\033[1;32m[?] Confirm launch (y/N): \033[0m").strip().lower()
    if confirm != 'y':
        print("\033[1;31m[!] Launch aborted by user.\033[0m")
        return

    # Expand environment variables and split safely
    expanded = os.path.expandvars(cmd)
    args = shlex.split(expanded)

    # Log the action
    with open("logs/audit.log", "a") as log:
        log.write(f"[{os.ctime()}] LAUNCH: {tool_config['name']} | CMD: {expanded}\n")

    # Execute
    try:
        subprocess.run(args, check=False)
    except Exception as e:
        print(f"\033[1;31m[!] Launch failed: {e}\033[0m")

def show_tool_info(tool_config):
    """
    Display tool description and dependencies.
    """
    print(f"\n\033[1;36m[TOOL INFO]\033[0m")
    print(f"Name        : {tool_config['name']}")
    print(f"Description : {tool_config['description']}")
    print(f"Launch Cmd  : {tool_config.get('launch_cmd', 'N/A')}")
    if tool_config.get("dependencies"):
        print("Dependencies:")
        for dep in tool_config["dependencies"]:
            print(f"  - {dep}")
