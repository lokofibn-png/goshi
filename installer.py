#!/usr/bin/env python3
import subprocess
import os
import sys

# ──────────────── Ethical Arsenal Constructor ────────────────
def install_tool(tool_config, env):
    pkg_mgr = env["pkg_manager"]  # ← FIXED: was "package_manager"
    name    = tool_config["name"]

    # 0. Guarantee python3-pip exists before any pip call
    if any("pip" in str(dep) for dep in tool_config.get("dependencies", [])) or \
       tool_config.get("python_packages"):
        ensure_pip(env)

    # 1. System packages
    for dep in tool_config.get("dependencies", []):
        if dep == "metasploit":
            install_msf(env)
            continue
        if dep in ("pip", "python3-pip"):        # already handled
            continue

        print(f"  [*] Installing {dep}…")
        cmd = []
        if pkg_mgr == "pkg":                     # Termux
            cmd = ["pkg", "install", "-y", dep]
        elif pkg_mgr == "apt":
            cmd = ["apt", "install", "-y", dep]
        elif pkg_mgr == "pacman":
            cmd = ["pacman", "-S", "--noconfirm", dep]
        elif pkg_mgr in ("yum", "dnf"):
            cmd = [pkg_mgr, "install", "-y", dep]

        if cmd:
            subprocess.run(cmd, stderr=subprocess.DEVNULL)

    # 2. Python packages via pip (always use -m pip for portability)
    for py_pkg in tool_config.get("python_packages", []):
        print(f"  [*] Pip-installing {py_pkg}…")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", py_pkg],
                       stderr=subprocess.DEVNULL)

    # 3. Source builds / clones
    if tool_config.get("source"):
        print(f"  [*] Cloning {name} from source…")
        for cmd in tool_config["source"]:
            subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)


def ensure_pip(env):
    """Bootstrap python3 -m pip if absent."""
    test = subprocess.run([sys.executable, "-m", "pip", "--version"],
                          capture_output=True, text=True)
    if test.returncode == 0:
        return

    print("  [*] Bootstrapping pip…")
    pkg_mgr = env["pkg_manager"]  # ← FIXED: was "package_manager"

    if pkg_mgr in ("apt", "pkg"):
        subprocess.run(["apt", "update"], stderr=subprocess.DEVNULL)
        subprocess.run(["apt", "install", "-y", "python3-pip"], stderr=subprocess.DEVNULL)
    elif pkg_mgr == "pacman":
        subprocess.run(["pacman", "-S", "--noconfirm", "python-pip"], stderr=subprocess.DEVNULL)
    elif pkg_mgr in ("yum", "dnf"):
        subprocess.run([pkg_mgr, "install", "-y", "python3-pip"], stderr=subprocess.DEVNULL)

    # Final safety net: get-pip.py
    if subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True).returncode != 0:
        subprocess.run([
            "curl", "-sSL", "https://bootstrap.pypa.io/get-pip.py", "-o", "/tmp/get-pip.py"
        ], stderr=subprocess.DEVNULL)
        subprocess.run([sys.executable, "/tmp/get-pip.py", "--user"], stderr=subprocess.DEVNULL)


def install_msf(env):
    """Metasploit special-case installer (Termux vs Linux)."""
    if env["os"] == "termux":
        deps = ["wget", "curl"]
        for d in deps:
            subprocess.run(["pkg", "install", "-y", d], stderr=subprocess.DEVNULL)
        subprocess.run([
            "wget", "-q", "https://raw.githubusercontent.com/Hax4us/Metasploit_termux/master/metasploit.sh",
            "-O", "/tmp/msf.sh"
        ], stderr=subprocess.DEVNULL)
        subprocess.run(["bash", "/tmp/msf.sh"], stderr=subprocess.DEVNULL)
    else:
        subprocess.run([
            "curl", "-sSL",
            "https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb",
            "-o", "/tmp/msfinstall"
        ], stderr=subprocess.DEVNULL)
        subprocess.run(["chmod", "+x", "/tmp/msfinstall"], stderr=subprocess.DEVNULL)
        subprocess.run(["/tmp/msfinstall"], stderr=subprocess.DEVNULL)
def get_merged_manifest():
    """Merge modular tools from tools/ folder + legacy JSON."""
    tools = {}
    
    # Load from tools/ directory
    import glob
    for path in glob.glob("tools/*.py"):
        if path.endswith(("reconnaissance.py", "__init__.py")):
            continue
        module_name = os.path.basename(path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "TOOL"):
            tools[module.TOOL["name"]] = module.TOOL
    
    # Legacy fallback
    if os.path.exists("config/tool_manifest.json"):
        import json
        with open("config/tool_manifest.json", "r") as f:
            tools.update(json.load(f))
    
    return tools

# Ensure directories exist on first import
os.makedirs("logs", exist_ok=True)
os.makedirs("config", exist_ok=True)

