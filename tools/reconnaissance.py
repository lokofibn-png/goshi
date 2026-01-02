#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  RECONNAISSANCE & INFORMATION GATHERING SUITE                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
This file aggregates all reconnaissance tools and provides a unified menu.
"""

import os
import glob
import importlib.util
import time

# ANSI Colors
C = {
    "r": "\033[1;31m", "g": "\033[1;32m", "y": "\033[1;33m",
    "b": "\033[1;34m", "m": "\033[1;35m", "c": "\033[1;36m",
    "x": "\033[0m"
}

def load_recon_tools():
    """Dynamically load all reconnaissance tool modules."""
    tools = {}
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filename in os.listdir(base_dir):
        if filename.endswith(".py") and filename not in ["reconnaissance.py", "__init__.py"]:
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(base_dir, filename))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "TOOL") and module.TOOL.get("category") == "reconnaissance":
                tools[module.TOOL["name"]] = module.TOOL
    
    return tools

def show_menu(env, master_tools, log_action, launch_tool):
    """Display interactive menu for all reconnaissance tools."""
    category_tools = load_recon_tools()
    
    if not category_tools:
        print(f"{C['r']}No reconnaissance tools found.{C['x']}")
        input("Press Enter...")
        return

    while True:
        os.system("clear" if env["os"] != "termux" else "clear")
        
        # Header
        print(f"{C['b']}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║          RECONNAISSANCE & INFORMATION GATHERING                   ║")
        print("║  ⚠️  ETHICAL USE ONLY – AUTHORIZED TARGETS ONLY                  ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{C['x']}\n")

        # Tool list
        tool_list = list(category_tools.items())
        for idx, (name, cfg) in enumerate(tool_list, 1):
            desc = cfg['description'][:55] + "..." if len(cfg['description']) > 55 else cfg['description']
            print(f" {C['y']}{idx:2d}.{C['x']} {C['c']}{name.upper():<12}{C['x']} – {desc}")
        
        print(f"\n {C['y']} 0.{C['x']} {C['r']}Return to Main Menu{C['x']}")
        print(f"\n{C['b']}{'='*70}{C['x']}")

        # Selection
        c = input(f"\n{C['g']}[?] Select Tool: {C['x']}").strip()
        if c == "0":
            break

        try:
            tool_name = tool_list[int(c) - 1][0]
            cfg = tool_list[int(c) - 1][1]
            
            # Import and execute
            base_dir = os.path.dirname(os.path.abspath(__file__))
            spec = importlib.util.spec_from_file_location(tool_name, os.path.join(base_dir, f"{tool_name}.py"))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            log_action("LAUNCH", tool_name)
            module.run(env, master_tools, log_action, launch_tool)
                
        except (IndexError, ValueError):
            print(f"{C['r']}Invalid selection.{C['x']}")
            time.sleep(1)
        except Exception as e:
            print(f"{C['r']}Error: {e}{C['x']}")
            log_action("ERROR", f"recon_menu_{str(e)}")
            time.sleep(1)

# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from os_detector import detect_environment
    from launchers import launch_tool
    
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    
    tools = load_recon_tools()
    show_menu(env, tools, log, launch_tool)
