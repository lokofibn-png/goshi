#!/usr/bin/env python3
import subprocess
import os
import sys

def install_tool(tool_config, env):
    pkg_mgr = env["pkg_manager"]
    name = tool_config["name"]
    
    # Install dependencies
    for dep in tool_config.get("dependencies", []):
        if dep == "metasploit":
            install_msf(env)
            continue
        
        print(f"  [*] Installing {dep}...")
        cmd = []
        
        if pkg_mgr == "pkg":
            cmd = ["pkg", "install", "-y", dep]
        elif pkg_mgr == "apt":
            cmd = ["apt", "install", "-y", dep]
        elif pkg_mgr == "pacman":
            cmd = ["pacman", "-S", "--noconfirm", dep]
        elif pkg_mgr == "yum" or pkg_mgr == "dnf":
            cmd = [pkg_mgr, "install", "-y", dep]
        
        if cmd:
            subprocess.run(cmd, stderr=subprocess.DEVNULL)
    
    # Install from source if needed
    if tool_config.get("source"):
        print(f"  [*] Cloning {name} from source...")
        for cmd in tool_config["source"]:
            subprocess.run(cmd.split(), stderr=subprocess.DEVNULL)

def install_msf(env):
    print("  [*] Installing Metasploit Framework...")
    if env["os"] == "termux":
        subprocess.run(["pkg", "install", "-y", "wget", "curl"], stderr=subprocess.DEVNULL)
        subprocess.run(["wget", "https://raw.githubusercontent.com/Hax4us/Metasploit_termux/master/metasploit.sh"], stderr=subprocess.DEVNULL)
        subprocess.run(["bash", "metasploit.sh"], stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["curl", "https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb", "-o", "msfinstall"], stderr=subprocess.DEVNULL)
        subprocess.run(["chmod", "+x", "msfinstall"], stderr=subprocess.DEVNULL)
        subprocess.run(["./msfinstall"], stderr=subprocess.DEVNULL)
