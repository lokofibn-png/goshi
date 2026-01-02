#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from os_detector import detect_environment
from installer import install_tool

# --- minimal logger ---------------------------------
def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")

# ----------------------------------------------------
def update_all():
    env = detect_environment()
    log("Starting standalone update protocol")

    # 1. self-update from git
    log("Git pull …")
    r = subprocess.run(["git", "pull"], capture_output=True, text=True)
    if r.returncode == 0 and "Already up to date" not in r.stdout:
        log("New code pulled")
    else:
        log("No new commits")

    # 2. upgrade Python deps listed in manifest
    log("Upgrading Python packages …")
    import json
    with open("config/tool_manifest.json") as f:
        tools = json.load(f)
    seen = set()
    for cfg in tools.values():
        for pkg in cfg.get("python_packages", []):
            if pkg in seen:
                continue
            seen.add(pkg)
            log(f"pip-upgrade {pkg}")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                           stderr=subprocess.DEVNULL)

    # 3. rebuild tools flagged auto_update
    log("Re-building auto-update tools …")
    for name, cfg in tools.items():
        if cfg.get("auto_update"):
            log(f"rebuild {name}")
            for cmd in cfg.get("source", []):
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)

    # 4. optional system upgrade
    pm = env["pkg_manager"]
    if pm == "apt":
        log("System package upgrade …")
        subprocess.run(["apt", "update"], stderr=subprocess.DEVNULL)
        subprocess.run(["apt", "upgrade", "-y"], stderr=subprocess.DEVNull)

    log("Standalone update complete")

# ----------------------------------------------------
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    update_all()
