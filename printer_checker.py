import socket

def check_printer(ip_address, port=9100, timeout=5):
    """
    Attempts to establish a TCP connection to the specified IP address of the printer
    and times out if the connection fails
    """

    try:
        socket.create_connection((ip_address, port), timeout)
        return True
    except (socket.timeout, OSError):
        return False

if __name__ == "__main__":
    target_ip = "192.168.90.108"
    result = check_printer(target_ip)
    print(f"Printer at {target_ip} is connected: {result}")