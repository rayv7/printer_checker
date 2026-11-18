import asyncio
import logging
import socket
import time
import ipaddress
import traceback

import printersList
import snmp_test


logging.basicConfig(
    filename="printer_checker.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def background_monitor():
    """
    This runs in the background and checks all the printers in the PRINTERS dictionary every 5 minutes.
    """
    print("Background printer monitoring started. Checking printers every 5 minutes...")
    while True:
        for name, ip in printersList.PRINTERS.items():
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
    print("=" * 60)
    print("<=================== RAY'S PRINTER CHECKER ===================>")
    print("=" * 60)
    print("\nWhat would you like to check today?")
    print("[1] Ping specific printer")
    print("[2] Check all listed printers")
    print("[3] Start background printer monitoring")
    print("[4] Check printer info")
    print("[5] Check printer status")
    selected = input("\n: ")
    select(selected)
    # TODO: Create logic for user input selection for the options
    #        and if statements to handle the different options

def select(selected):
    """
    Handles user input
    """
    # TODO: implement user input error handling
    try:
        selection = int(selected)
        if 1 <= selection <= 5:
            if selection == 1:
                ping_specific_printer()
            elif selection == 2:
                check_all_printers()
            elif selection == 3:
                #TODO: Improve this
                background_monitor()
                pass
            elif selection == 4:
                check_printer_info()
            elif selection == 5:
                check_printer_status()
        else:
            print(f"\nPlease enter a number between 1 and 5\n")
            time.sleep(1)
            interface()

    except Exception as e:
        time.sleep(1)
        print(f"[ERROR]: Please enter a valid integer ({selected}) is not valid\n")
        print(f"[ERROR]: {e}")
        time.sleep(2)   
        interface()

def ping_specific_printer():
    printersList.get_printer_list()
    target_ip = input("\nEnter printer's IP address: ")
    valid = validate_ip(target_ip)
    if not valid:
        time.sleep(1)
        print(f"\nThe ip({target_ip}) you have provided is not valid. Please try again.\n")
        time.sleep(2)
        select(1)
    else:
        result = check_printer(target_ip)
        if not result:
            print(f"\n[ERROR]: The printer at ({target_ip}) is not connected or it is not a valid printer ip. Please check the ip and try again.")
        else:
            print(f"\nPrinter at {target_ip} is connected: {result}")
    
def check_all_printers():
    for name, ip in printersList.PRINTERS.items():
        result = check_printer(ip)
        print(f"\nPrinter at {ip}({name}) is connected: {result}")
        time.sleep(1)
    
def check_printer_info():
    printersList.get_printer_list()
    target_ip = input(f"\nInput target printer or IP address(1 - {len(printersList.PRINTERS)}): ".format(len(printersList.PRINTERS)))
    valid = validate_ip(target_ip)
    if not valid:
        try:
            target_ip = printersList.map_to_printer(target_ip)
            if target_ip is None:
                check_printer_info()
            else:
                asyncio.run(snmp_test.get_printer_info(target_ip))
        except ValueError as e:
            print("\nTarget not found\n")
            print(f"\nThe ip({target_ip}) you have provided is not valid. Please try again.\n")
            print(f"[error]: {e}")
            check_printer_info()
    else:
        print(f"\nRetrieving printer information for {target_ip}...\n")
        asyncio.run(snmp_test.get_printer_info(target_ip))

def check_printer_status():
    printersList.get_printer_list()
    target_ip = input(f"\nInput target printer or IP address(1 - {len(printersList.PRINTERS)}): ".format(len(printersList.PRINTERS)))
    valid = validate_ip(target_ip)
    if not valid:
        try:
            target_ip = printersList.map_to_printer(target_ip)
            if target_ip is None:
                check_printer_status()
            else:
                asyncio.run(snmp_test.get_printer_status(target_ip))
        except ValueError as e:
            print("\nTarget not found\n")
            print(f"\nThe ip({target_ip}) you have provided is not valid. Please try again.\n")
            print(f"[error]: {e}")
            check_printer_status()
    else:
        print(f"\nRetrieving printer status for {target_ip}...\n")
        asyncio.run(snmp_test.get_printer_status(target_ip))

if __name__ == "__main__":
    interface()
    # TODO: Add back buttons