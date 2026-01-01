#!/usr/bin/env python3
import os
import platform
import subprocess

def detect_environment():
    env = {"os": "unknown", "distro": "unknown", "pkg_manager": "unknown"}
    
    # Detect Termux
    if "com.termux" in os.getenv("PREFIX", ""):
        env["os"] = "termux"
        env["distro"] = "Termux Android"
        env["pkg_manager"] = "pkg"
        return env
    
    # Detect standard Linux
    env["os"] = "linux"
    
    # Detect distro
    try:
        with open("/etc/os-release", "r") as f:
            lines = f.read().lower()
            if "kali" in lines:
                env["distro"] = "Kali Linux"
            elif "ubuntu" in lines:
                env["distro"] = "Ubuntu"
            elif "arch" in lines:
                env["distro"] = "Arch Linux"
            elif "fedora" in lines:
                env["distro"] = "Fedora"
            else:
                env["distro"] = platform.system()
    except:
        env["distro"] = platform.system()
    
    # Detect package manager
    for pm in ["apt", "pacman", "yum", "dnf", "zypper"]:
        if subprocess.run(["which", pm], capture_output=True).returncode == 0:
            env["pkg_manager"] = pm
            break
    
    return env
