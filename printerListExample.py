"""
Rename to printersList.py and you're good to go
This file contains a list of printers and their corresponding IP addresses.
"""

PRINTERS = {
    "CEO" : "192.168.93.24",
    "Cash Office": "192.168.90.16",
    "Legal": "192.168.94.5",
    "HR": "192.168.94.246",
    "Environment": "192.168.90.137",
    "Technical": "192.168.93.197"
}

def get_printer_list():
    print("\nLISTED PRINTERS")
    print("=" * 35)
    for n, (name, ip) in enumerate(PRINTERS.items()):
        print(f"[{n+1}]: {name:<12}: {ip}")
    print("=" * 35)

def map_to_printer(input):
    if 1 <= int(input) <= len(PRINTERS):
        for n, (name, ip) in enumerate(PRINTERS.items()):
            if input == str(n+1):
                print(f"\nSelected Printer: {name} ({ip})\n")
                return ip
    else:
        print(f"\nPlease enter a number between 1 and {len(PRINTERS)}")
        return None
