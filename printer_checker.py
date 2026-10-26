import socket

PRINTERS = {
    "Cash Office": "192.168.90.180",
    "Legal": "192.168.90.181",
    "HR": "192.168.90.20",
    "Environment": "192.168.90.106",
    "Technical": "192.168.90.125"
}

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

def interface():
    """
    The cli interface for the printer checker.
    it's the first thing that pops up when the script is run.
    Welcomes the user and asks for the IP address of the printer to check.
    """
    print("\t==============================================================")
    print("\t<=================== RAY'S PRINTER CHECKER ===================>")
    print("\t==============================================================")
    print("\nWhat would you like to check today?")
    print("[1] Ping specific printer")
    print("[2] Check all listed printers")
    print("[3] Coming soon...")
    print("[4] Coming soon...")
    selection = input("\n: ")
    select(selection)
    # TODO: Create logic for user input selection for the options
    #        and if statements to handle the different options

def select(selection):
    """
    Handles user input
    """
    # TODO: implement user input error handling
    if selection == "1":
        target_ip = input("\nEnter printer's IP address: ")
        result = check_printer(target_ip)
        print(f"\nPrinter at {target_ip} is connected: {result}")
    elif selection == "2":
        for name, ip in PRINTERS.items():
            result = check_printer(ip)
            print(f"\nPrinter at {ip} ({name}) is connected: {result}")

if __name__ == "__main__":
    interface()