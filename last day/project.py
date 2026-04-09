from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime

# =========================
# Device List (Edit This)
# =========================
devices = [
    {"device_type": "cisco_ios", "host": "192.168.1.1", "name": "router1"},
    {"device_type": "cisco_ios", "host": "192.168.1.2", "name": "router2"},
]

# =========================
# Get User Credentials
# =========================
username = input("Enter SSH Username: ")
password = getpass("Enter SSH Password: ")

# =========================
# Create Report File
# =========================
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"Audit_Report_{date_str}.txt"

report = open(filename, "w")
report.write("--- Network Device Audit Report ---\n\n")

# =========================
# Audit Function
# =========================
def audit_device(device):
    device_info = {
        "device_type": device["device_type"],
        "host": device["host"],
        "username": username,
        "password": password,
    }

    try:
        connection = ConnectHandler(**device_info)

        # Get running config
        config = connection.send_command("show running-config")

        # =========================
        # Checks
        # =========================

        # 1. Telnet Check
        if "transport input telnet" in config:
            telnet_status = "Telnet is enabled"
        else:
            telnet_status = "Telnet is disabled"

        # 2. HTTP Server Check
        if "ip http server" in config:
            http_status = "HTTP server is enabled"
        else:
            http_status = "HTTP server is disabled"

        # 3. SNMP Check
        if "snmp-server community public" in config or \
           "snmp-server community private" in config:
            snmp_status = "Default SNMP community strings found"
        else:
            snmp_status = "No default SNMP community strings found"

        connection.disconnect()

        return telnet_status, http_status, snmp_status

    except Exception as e:
        return "Connection failed", "Connection failed", "Connection failed"

# =========================
# Run Audit
# =========================
for device in devices:
    print(f"Auditing {device['name']}...")

    telnet, http, snmp = audit_device(device)

    report.write(f"Device: {device['name']}\n")
    report.write(f"- Telnet Status: {telnet}\n")
    report.write(f"- HTTP Server Status: {http}\n")
    report.write(f"- SNMP Status: {snmp}\n\n")

report.close()

print(f"\nAudit report saved to {filename}")