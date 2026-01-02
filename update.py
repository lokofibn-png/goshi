#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import json
from os_detector import detect_environment

# ──────────────── Logger & Colors ────────────────
C = {
    "r": "\033[1;31m", "g": "\033[1;32m", "y": "\033[1;33m",
    "b": "\033[1;34m", "m": "\033[1;35m", "c": "\033[1;36m",
    "x": "\033[0m"
}

def log(msg, level="info"):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    colors = {"info": "c", "ok": "g", "warn": "y", "err": "r"}
    print(f"{C[colors.get(level, 'c')]}{ts}{C['x']} {msg}")

# ──────────────── Git Handler ────────────────
def git_pull():
    """Pull with full transparency."""
    log("Checking if this is a git repository...", "info")
    if not os.path.exists(".git"):
        log("Not a git repository. Skipping pull.", "warn")
        return False

    log("Fetching remote changes...", "info")
    fetch = subprocess.run(["git", "fetch"], capture_output=True, text=True)
    if fetch.returncode != 0:
        log(f"Fetch failed: {fetch.stderr}", "err")
        return False

    # Check if we're behind
    status = subprocess.run(["git", "status", "--porcelain", "-b"], capture_output=True, text=True)
    if "behind" not in status.stdout:
        log("Already up-to-date with remote.", "ok")
        return True

    log("Changes detected. Pulling...", "warn")
    pull = subprocess.run(["git", "pull", "--stat"], capture_output=True, text=True)
    if pull.returncode == 0:
        log("Git pull successful.", "ok")
        if pull.stdout:
            print(f"\n{C['y']}Changed files:{C['x']}\n{pull.stdout}")
        return True
    else:
        log(f"Pull failed: {pull.stderr}", "err")
        return False

# ──────────────── Python Package Updater ────────────────
def upgrade_python_packages(tools):
    """Upgrade every pip package listed in any tool."""
    ensured = set()
    upgrades = 0

    for name, cfg in tools.items():
        for pkg in cfg.get("python_packages", []):
            if pkg in ensured:
                continue
            ensured.add(pkg)

            # Get current version
            ver = subprocess.run([sys.executable, "-m", "pip", "show", pkg],
                                 capture_output=True, text=True)
            old_ver = "unknown"
            if ver.returncode == 0:
                for line in ver.stdout.splitlines():
                    if line.startswith("Version:"):
                        old_ver = line.split()[1]
                        break

            log(f"Upgrading {pkg} (was {old_ver})...", "info")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                                    capture_output=True, text=True)

            if result.returncode == 0:
                log(f"{pkg} upgraded successfully.", "ok")
                upgrades += 1
            else:
                log(f"{pkg} upgrade failed: {result.stderr}", "err")

    if upgrades == 0:
        log("No Python packages needed upgrading.", "ok")
    else:
        log(f"Upgraded {upgrades} Python packages.", "ok")

# ──────────────── Tool Rebuilder ────────────────
def rebuild_tools(tools, env):
    """Rebuild tools flagged for auto-update."""
    rebuilt = 0

    for name, cfg in tools.items():
        if cfg.get("auto_update"):
            log(f"Rebuilding {name}...", "info")
            success = True
            for cmd in cfg.get("source", []):
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    log(f"{name} rebuild step failed: {result.stderr}", "err")
                    success = False
                    break
            if success:
                log(f"{name} rebuilt successfully.", "ok")
                rebuilt += 1

    if rebuilt == 0:
        log("No tools needed rebuilding.", "ok")
    else:
        log(f"Rebuilt {rebuilt} tools.", "ok")

# ──────────────── System Updater ────────────────
def system_upgrade(env):
    """Offer optional system package upgrade."""
    pm = env.get("pkg_manager", "unknown")
    if pm == "unknown":
        log("Cannot determine package manager. Skipping system upgrade.", "warn")
        return

    log("System package upgrade available.", "warn")
    ans = input(f"\n{C['y']}Upgrade system packages via {pm}? (may be large) [y/N]: {C['x']}").strip().lower()
    if ans != "y":
        log("System upgrade skipped by user.", "info")
        return

    log(f"Running {pm} upgrade...", "info")
    if pm == "apt":
        subprocess.run([pm, "update"], stderr=subprocess.DEVNULL)
        subprocess.run([pm, "upgrade", "-y"], stderr=subprocess.DEVNULL)
    elif pm == "pacman":
        subprocess.run([pm, "-Syu", "--noconfirm"], stderr=subprocess.DEVNULL)
    elif pm in ("yum", "dnf"):
        subprocess.run([pm, "upgrade", "-y"], stderr=subprocess.DEVNULL)
    elif pm == "pkg":
        subprocess.run([pm, "upgrade", "-y"], stderr=subprocess.DEVNULL)

    log("System packages upgraded.", "ok")

# ──────────────── Main Update Orchestrator ────────────────
def update_all():
    """Run the full update protocol."""
    log("Starting standalone update protocol", "info")
    env = detect_environment()

    # 1. Git pull (with full transparency)
    git_ok = git_pull()

    # 2. Load merged tool manifest (modular + legacy)
    try:
        tools = get_merged_tools()
    except Exception as e:
        log(f"Failed to load tools manifest: {e}", "err")
        tools = {}

    # 3. Python packages
    if tools:
        upgrade_python_packages(tools)

    # 4. Rebuild tools
    if tools:
        rebuild_tools(tools, env)

    # 5. System upgrade (optional)
    system_upgrade(env)

    log("Update protocol complete.", "ok")
    log("Restart main.py to load new code.", "warn")


def get_merged_tools():
    """Merge modular tools (tools/*.py) + legacy JSON manifest."""
    tools = {}

    # Load legacy JSON manifest if it exists
    if os.path.exists("config/tool_manifest.json"):
        with open("config/tool_manifest.json") as f:
            tools.update(json.load(f))

    # Load modular tools
    for path in glob.glob("tools/*.py"):
        if path.endswith("__init__.py"):
            continue
        module_name = path[:-3].replace("/", ".")
        try:
            module = __import__(module_name, fromlist=["TOOLS"])
            if hasattr(module, "TOOLS"):
                for name, cfg in module.TOOLS.items():
                    cfg["category"] = module_name.split(".")[-1]
                    tools[name] = cfg
        except Exception as e:
            log(f"Failed to load {path}: {e}", "err")

    return tools


# ──────────────── Entry Point ────────────────
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    update_all()
