#!/usr/bin/env python3
import os
import sys
import time
import platform
import subprocess
from os_detector import detect_environment
from installer import install_tool
from launchers import launch_tool, show_tool_info

# --- ASCII Boot Screen --------------------------------------------------
def boot_screen():
    print(r"""
\033[1;32m
    ╔════════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║     ██████╗ ███████╗ █████╗ ███████╗ █████╗ ██╗  ██╗███████╗      ║
    ║     ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██╔════╝      ║
    ║     ██████╔╝█████╗  ███████║███████╗███████║█████╔╝ █████╗        ║
    ║     ██╔══██╗██╔══╝  ██╔══██║╚════██║██╔══██║██╔═██╗ ██╔══╝        ║
    ║     ██║  ██║███████╗██║  ██║███████║██║  ██║██║  ██╗███████╗      ║
    ║     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝      ║
    ║                                                                    ║
    ║          "We are the ghosts in the machine, testing the locks"     ║
    ║                                                                    ║
    ╚════════════════════════════════════════════════════════════════════╝
    \033[0m
    """)
    time.sleep(2)
# --- FSociety Boot Screen (exact bytes you cloned) ----------------------
def boot_screen():
    print(r"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N   MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM   N           XX
XX            +  .sMNNNNNMMMMMN+   N    N   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    """)
    print(r"""
\033[1;32m
    \033[0m
    """)
    time.sleep(1.5)
# --- Ghost Protocol Class ----------------------------------------------
class GhostProtocol:
    def __init__(self):
        self.env = detect_environment()
        self.tools = self.load_manifest()
        self.audit_log = "logs/audit.log"
        os.makedirs("logs", exist_ok=True)

    def load_manifest(self):
        import json
        with open("config/tool_manifest.json", "r") as f:
            return json.load(f)

    def log_action(self, action, tool):
        with open(self.audit_log, "a") as f:
            f.write(f"[{time.ctime()}] {action}: {tool} | USER: {os.getenv('USER')} | PID: {os.getpid()}\n")

    def display_menu(self):
        while True:
            os.system("clear" if self.env["os"] != "termux" else "clear")
            print(r"""
\033[1;32m
                  .o88o.                               o8o                .
                  888 `"                               `"'              .o8
                 o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
                  888    d88(  "8 d88' 88b d88' `"Y8  888  d88' `88b   888    `88.  .8'
                  888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
                  888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
                 o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                           .o...P'
                                                                           XER0\033[0m
            """)
                     print(f"\n\033[1;36m[ENVIRONMENT: {self.env['distro']} | PKG: {self.env['pkg_manager']}]\033[0m")
            print("\033[1;32mPrivacy is a myth—choose your weapon\033[0m")
            print("\033[1;33m[MAIN MENU]\033[0m")
            print("=" * 50)
            print("1.  Reconnaissance & Information Gathering")
            print("2.  Vulnerability Assessment")
            print("3.  Exploitation Frameworks")
            print("4.  Post-Exploitation & Persistence")
            print("5.  Password Attacks")
            print("6.  Wireless Attacks")
            print("7.  Web Application Testing")
            print("8.  Network Analysis")
            print("9.  Social Engineering")
            print("10. Custom Attack Vectors (Ethical Testing Only)")
            print("11. Install/Update All Tools")
            print("12. Audit Trail")
            print("13. Update / Refresh Arsenal (git pull + pip upgrade + tool rebuild)")
            print("0.  Exit to Void")
            print("=" * 50)

            choice = input("\n\033[1;32m[?] Select Module: \033[0m").strip()
            self.route_choice(choice)

    def route_choice(self, choice):
        if choice == "0":
            print("\n\033[1;31m[!] Terminating ghost protocol...\033[0m")
            sys.exit(0)
        elif choice == "13":
            self.update_arsenal()
        elif choice == "1":
            self.recon_menu()
        elif choice == "2":
            self.vuln_menu()
        elif choice == "3":
            self.exploit_menu()
        elif choice == "10":
            self.custom_attacks_menu()
        elif choice == "11":
            self.install_all()
        elif choice == "12":
            self.show_audit()
        else:
            print("\n\033[1;31m[!] Module not yet implemented\033[0m")
            time.sleep(1)

    # (sub-menu stubs & update engine remain identical to last complete paste)
    def recon_menu(self):
        while True:
            print("\n\033[1;34m[RECONNAISSANCE SUITES]\033[0m")
            print("- " * 30)
            tools = ["nmap", "maltego", "shodan", "recon-ng", "gobuster", "dirb"]
            for idx, tool in enumerate(tools, 1):
                print(f"{idx}. {tool.upper()} - {self.tools[tool]['description']}")
            print("0. Back")
            c = input("\n[?] Tool: ").strip()
            if c == "0":
                break
            try:
                tool_name = tools[int(c) - 1]
                self.log_action("LAUNCH", tool_name)
                launch_tool(self.tools[tool_name], self.env)
            except (IndexError, ValueError):
                pass

    def custom_attacks_menu(self):
        print("\n\033[1;35m[CUSTOM ATTACK VECTORS]\033[0m")
        print("⚠️  \033[1;33mETHICAL TESTING ONLY - AUTHORIZED TARGETS ONLY\033[0m")
        print("=" * 60)
        print("1. Spectral DDoS Simulator (Localhost Stress Test)")
        print("2. SQL Wraith (Vulnerable WebApp Demo + Scanner)")
        print("3. Packet Phantom (ICMP/UDP/TCP Crafting)")
        print("4. Hash Ritual (Automated Cracking Orchestrator)")
        print("0. Return to Mainframe")
        c = input("\n[?] Vector: ").strip()
        if c == "1":
            self.log_action("CUSTOM_DDOS", "spectral_ddos.py")
            os.system("python3 custom_tools/spectral_ddos.py")
        elif c == "2":
            self.log_action("CUSTOM_SQLI", "sql_wraith.py")
            os.system("python3 custom_tools/sql_wraith.py")
        elif c == "3":
            self.log_action("CUSTOM_PACKET", "packet_phantom.py")
            os.system("python3 custom_tools/packet_phantom.py")
        elif c == "4":
            self.log_action("CUSTOM_HASH", "hash_ritual.py")
            os.system("python3 custom_tools/hash_ritual.py")

    def install_all(self):
        print("\n\033[1;33m[!] Installing full suite. This will take time...\033[0m")
        confirm = input("Type 'HELL YES' to confirm: ").strip()
        if confirm != "HELL YES":
            return
        for tool_name, config in self.tools.items():
            print(f"\n[*] Installing {tool_name}...")
            self.log_action("INSTALL", tool_name)
            install_tool(config, self.env)
        print("\n\033[1;32m[✓] Ghost protocol fully armed.\033[0m")

    def show_audit(self):
        print("\n\033[1;36m[ETHICAL USAGE AUDIT TRAIL]\033[0m")
        print("- " * 30)
        try:
            with open(self.audit_log, "r") as f:
                print(f.read())
        except FileNotFoundError:
            print("No audit trail yet. Actions are being logged.")
        input("\nPress Enter to continue...")

    def update_arsenal(self):
        print("\n\033[1;35m[UPDATE PROTOCOL] Syncing with upstream & upgrading tools...\033[0m")
        self.log_action("UPDATE", "arsenal")
        # 1. Git pull
        print("\n[*] Git pull...")
        g = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if g.returncode == 0 and "Already up to date" not in g.stdout:
            print("\033[1;32m[✓] New code pulled.\033[0m")
        else:
            print("[*] No new commits.")
        # 2. Python packages
        print("\n[*] Upgrading Python dependencies...")
        ensured = set()
        for tool_name, cfg in self.tools.items():
            for py_pkg in cfg.get("python_packages", []):
                if py_pkg in ensured:
                    continue
                ensured.add(py_pkg)
                print(f"    upgrading {py_pkg} ...")
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", py_pkg],
                               stderr=subprocess.DEVNULL)
        # 3. Re-build auto-update tools
        print("\n[*] Re-building tools that request auto-update ...")
        for tool_name, cfg in self.tools.items():
            if cfg.get("auto_update"):
                print(f"    rebuilding {tool_name} ...")
                for cmd in cfg["source"]:
                    subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
        # 4. Optional system upgrade
        ans = input("\n[?] Also upgrade system packages? (may be large) (y/N): ").strip().lower()
        if ans == "y":
            print("\n[*] System upgrade ...")
            pm = self.env["pkg_manager"]
            if pm == "apt":
                subprocess.run(["apt", "update"], stderr=subprocess.DEVNULL)
                subprocess.run(["apt", "upgrade", "-y"], stderr=subprocess.DEVNULL)
            elif pm == "pacman":
                subprocess.run(["pacman", "-Syu", "--noconfirm"], stderr=subprocess.DEVNULL)
            elif pm in ("yum", "dnf"):
                subprocess.run([pm, "upgrade", "-y"], stderr=subprocess.DEVNULL)
            elif pm == "pkg":  # termux
                subprocess.run(["pkg", "upgrade", "-y"], stderr=subprocess.DEVNULL)
        print("\n\033[1;32m[✓] Arsenal refreshed. Restart main.py to load any new code.\033[0m")
        input("\nPress Enter to return to menu...")

    def vuln_menu(self): pass
    def exploit_menu(self): pass

# --- Cathedral Doors ----------------------------------------------------
if __name__ == "__main__":
    boot_screen()
    ghost = GhostProtocol()
    ghost.display_menu()
