import logging
import socket
import time
import ipaddress


logging.basicConfig(
    filename="printer_checker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PRINTERS = {
    "Cash Office": "192.168.90.180",
    "Legal": "192.168.90.24",
    "HR": "192.168.90.20",
    "Environment": "192.168.90.106",
    "Technical": "192.168.90.125"
}

def background_monitor():
    """
    This runs in the background and checks all the printers in the PRINTERS dictionary every 5 minutes.
    """
    print("Background printer monitoring started. Checking printers every 5 minutes...")
    while True:
        for name, ip in PRINTERS.items():
            result = check_printer(ip)
            if result:
                logging.info(f"Printer at {ip} ({name}) is connected: {result}")
            else:
                logging.warning(f"Printer at {ip} ({name}) is connected: {result}")
        time.sleep(3)

def check_printer(ip_address, port=9100, timeout=10):
    """
    Attempts to establish a TCP connection to the specified IP address of the printer
    and times out if the connection fails
    """

    try:
        socket.create_connection((ip_address, port), timeout)
        return True
    except (socket.timeout, OSError) as e:
        logging.error(f"Error connecting to printer at {ip_address}: {e}")
        return False

def validate_ip(ipa):
    """
    Validates if the input is actually an ip
    """
    try:
        ipaddress.ip_address(ipa)
        return True
    except ValueError:
        return False

def interface():
    """
    The cli interface for the printer checker.
    it's the first thing that pops up when the script is run.
    Welcomes the user and asks for the IP address of the printer to check.
    """
    print("==============================================================")
    print("<=================== RAY'S PRINTER CHECKER ===================>")
    print("==============================================================")
    print("\nWhat would you like to check today?")
    print("[1] Ping specific printer")
    print("[2] Check all listed printers")
    print("[3] Start background printer monitoring")
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
        valid = validate_ip(target_ip)
        if not valid:
            print(f"\nThe ip({target_ip}) you have provided is not valid. Please try again.\n")
            interface()
        else:
            result = check_printer(target_ip)
            if not result:
                print(f"\n[ERROR]: The printer at ({target_ip}) is not connected or it is not a valid printer ip. Please check the ip and try again")
            else:
                print(f"\nPrinter at {target_ip} is connected: {result}")
    elif selection == "2":
        for name, ip in PRINTERS.items():
            result = check_printer(ip)
            print(f"\nPrinter at {ip} ({name}) is connected: {result}")
    elif selection == "3":
        background_monitor()
        pass

if __name__ == "__main__":
    interface()