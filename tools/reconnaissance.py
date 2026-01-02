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

# ANSI Colors
C = {
    "r": "\033[1;31m", "g": "\033[1;32m", "y": "\033[1;33m",
    "b": "\033[1;34m", "m": "\033[1;35m", "c": "\033[1;36m",
    "x": "\033[0m"
}

def load_recon_tools():
    """Dynamically load all reconnaissance tool modules."""
    tools = {}
    for path in glob.glob("tools/*.py"):
        if path.endswith(("reconnaissance.py", "__init__.py")): 
            continue
        module_name = os.path.basename(path)[:-3]
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "TOOL") and module.TOOL.get("category") == "reconnaissance":
            tools[module.TOOL["name"]] = module.TOOL
    
    return tools

def show_menu(env, master_tools, log_action, launch_tool):
    """Display interactive menu for all reconnaissance tools."""
    # Load fresh from disk to catch updates
    category_tools = load_recon_tools()
    
    if not category_tools:
        print(f"{C['r']}No reconnaissance tools found.{C['x']}")
        input("Press Enter...")
        return

    while True:
        os.system("clear" if env["os"] != "termux" else "clear")
        
        print(f"{C['b']}")
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║  RECONNAISSANCE & INFORMATION GATHERING                        ║")
        print("║  ⚠️  ETHICAL USE ONLY - AUTHORIZED TARGETS ONLY               ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print(f"{C['x']}")

        for idx, (name, cfg) in enumerate(category_tools.items(), 1):
            print(f"{C['y']}{idx:2d}. {C['c']}{name.upper():<12}{C['x']}{C['y']} - {cfg['description'][:50]}...{C['x']}")
        print(f"{C['y']} 0. {C['r']}Return{C['x']}")
        print(f"{C['b']}{'=' * 64}{C['x']}")

        c = input(f"\n{C['g']}[?] Select Tool: {C['x']}").strip()
        if c == "0":
            break

        try:
            tool_name = list(category_tools.keys())[int(c) - 1]
            cfg = category_tools[tool_name]
            
            # Import the module and run its custom launcher
            spec = importlib.util.spec_from_file_location(tool_name, f"tools/{tool_name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, "run"):
                module.run(env, master_tools, log_action, launch_tool)
            else:
                # Fallback to generic launch
                log_action("LAUNCH", tool_name)
                launch_tool(cfg, env)
                
        except Exception as e:
            print(f"{C['r']}Error: {e}{C['x']}")
            time.sleep(1)
