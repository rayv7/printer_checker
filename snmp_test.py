from pysnmp.hlapi import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd
)

def get_printer_info(ip_address):
    """
    Retrieves printer information using SNMP from the specified IP address.
    """
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0),
        UdpTransportTarget((ip_address, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"[NETWORK ERROR]: {errorIndication}")
    elif errorStatus:
        print(f"[SNMP ERROR]: {errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        print("[SUCCESS]: Retrieved printer information:")
        for varBind in varBinds:
            print(f"Info: {varBind[0].prettyPrint()} = {varBind[1].prettyPrint()}")

if __name__ == "__main__":
    test_ip = "192.168.90.121"
    print(f"Querying {test_ip} via SNMP...")
    get_printer_info(test_ip)