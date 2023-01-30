import socket
import sys

PROXY_HOST = "proxy.example.com" # Replace with the hostname of your proxy gateway
PROXY_PORT = 8080 # Replace with the port number of your proxy gateway

HOST_PORT_PAIRS = [
    ("192.168.1.1", 80),
    ("192.168.1.2", 443),
    ("192.168.1.3", 22),
    # Add more IP addresses and port numbers as needed
]

def is_port_open_through_proxy(host, port, proxy_host, proxy_port):
    try:
        with socket.create_connection((proxy_host, proxy_port), timeout=5) as sock:
            # Send a HTTP CONNECT request to the proxy to establish a tunnel
            sock.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
            response = sock.recv(1024).decode()
            if "200 Connection established" in response:
                # Port is open
                return True
            else:
                # Port is closed
                return False
    except Exception as e:
        # Connection to the proxy gateway failed
        print(f"Error: {e}", file=sys.stderr)
        return False

for host, port in HOST_PORT_PAIRS:
    if is_port_open_through_proxy(host, port, PROXY_HOST, PROXY_PORT):
        print(f"Port {port} on IP address {host} is open")
    else:
        print(f"Port {port} on IP address {host} is closed")
