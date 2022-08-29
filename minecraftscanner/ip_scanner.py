"""
ip_scanner.py
Scans every single ip address for minecraft servers
"""
import masscan
import random
from mcstatus import JavaServer

def scan(ip_range: str) -> list:
    """
    scan for minecraft servers
    """
    port_scanner = masscan.PortScanner()

    try:
        port_scanner.scan(ip_range, ports='25565', arguments='--max-rate 10000', sudo=True)
    except masscan.NetworkConnectionError:
        # print(f"Network connection error in {ip_range}")
        return []
    
    hosts = port_scanner.scan_result['scan']
    
    servers = []

    for ip in hosts:
        status = minecraft_status(ip)
        if status is not None:
            servers.append(status)

    return servers

def minecraft_status(ip: str):
    """
    check if minecraft server is online
    """
    try:
        # status = JavaServer(ip).status()
        status = JavaServer(ip).status()
        raw = status.raw
        raw["ip"] = ip
        print(raw)
        return raw
    except ConnectionError:
        # print(f"Connection error in {ip}")
        return None
    except OSError:
        # print(f"OS error in {ip}")
        return None
    
def generate_ip_range():
    """
    generate ip range
    """
    A = list(range(1,0xff))
    B = list(range(1,0xff))
    random.shuffle(A)
    random.shuffle(B)
    ip_ranges = []

    for a in A:
        for b in B:
            ip_range = f"{a}.{b}.0.0/16"
            ip_ranges.append(ip_range)
    
    random.shuffle(ip_ranges)
    return ip_ranges

if __name__ == '__main__':
    minecraft_status("200.89.178.245")
    # ip_range = generate_ip_range()
    # print(scan(ip_range[0]))