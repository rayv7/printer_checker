import asyncio
from pysnmp.hlapi.v1arch.asyncio import (
    SnmpDispatcher,
    CommunityData,
    UdpTransportTarget,
    ObjectType,
    ObjectIdentity,
    get_cmd
)

async def get_printer_info(ip_address):
    """
    Retrieves printer information using SNMP from the specified IP address.
    """
    transport_target = await UdpTransportTarget.create((ip_address, 161))

    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        SnmpDispatcher(),
        CommunityData('public', mpModel=0),
        transport_target,
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    )

    if errorIndication:
        print(f"[NETWORK ERROR]: {errorIndication}")
    elif errorStatus:
        print(f"[SNMP ERROR]: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        print("[SUCCESS]: Retrieved printer information:")
        raw_data = varBinds[0][1].prettyPrint()
        parsed_info = parse_sys_descr(raw_data)
        print("\n" + "=" * 34)
        print("\tPRINTER INFORMATION")
        print("=" * 34)
        for key, value in parsed_info.items():
            print(f"{key:<15}: {value}")
        print("=" * 34 + "\n")

async def check_printer_status(ip_address):
    """
    Checks the printer status using SNMP from the specified IP address.
    """
    transport_target = await UdpTransportTarget.create((ip_address, 161))

    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        SnmpDispatcher(),
        CommunityData('public', mpModel=0),
        transport_target,
        ObjectType(ObjectIdentity('HOST-RESOURCES-MIB', 'hrPrinterStatus', 1))
    )

    if errorIndication:
        print(f"[NETWORK ERROR]: {errorIndication}")
    elif errorStatus:
        print(f"[SNMP ERROR]: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        status_code = varBinds[0][1].prettyPrint()
        print(f"[SUCCESS]: Printer status for ({ip_address}): {status_code}")

def status_decoder(status_code):
    """
    Decodes the printer status code into a human-readable format.
    """
    status_map = {
        1: "Other",
        2: "Unknown",
        3: "Idle / Ready",
        4: "Printing",
        5: "Warming up",
        6: "Stopped / Error"
    }
    return status_map.get(int(status_code), "Unknown")

def parse_sys_descr(raw_text):
    # Default structure
    info = {
        "Model": "Unknown",
        "Serial Number": "Unknown",
        "Firmware": "Unknown",
        "Service ID": "Unknown",
    }
    
    # Split by comma
    parts = [p.strip() for p in raw_text.split(",")]
    
    for part in parts:
        if "PID:" in part:
            info["Model"] = part.replace("PID:", "").strip()
        elif "SN:" in part:
            info["Serial Number"] = part.replace("SN:", "").strip()
        elif "FN:" in part:
            info["Firmware"] = part.replace("FN:", "").strip()
        elif "SVCID:" in part:
            info["Service ID"] = part.replace("SVCID:", "").strip()
            
    return info

if __name__ == "__main__":
    test_ip = "192.168.93.121"  
    print(f"Querying {test_ip} via SNMP...\n")
    asyncio.run(check_printer_status(test_ip))
