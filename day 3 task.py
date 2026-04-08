import re
import csv
import json
from collections import Counter
from datetime import datetime

entries = []
malformed = 0
total = 0

action_count = Counter()
port_count = Counter()
ip_count = Counter()

# Regex pattern to match valid logs
pattern = re.compile(
    r"(.+?)\s+(ACCEPT|DROP)\s+(TCP|UDP|ICMP)\s+SRC=(\S+)\s+SPT=(\d+)\s+DST=(\S+)\s+DPT=(\d+)\s+LEN=(\d+)"
)

with open("firewall.log", "r") as file:
    for line in file:
        total += 1
        line = line.strip()

        match = pattern.match(line)
        if not match:
            malformed += 1
            continue

        timestamp, action, protocol, src_ip, src_port, dst_ip, dst_port, length = match.groups()

        entry = {
            "timestamp": timestamp,
            "action": action,
            "protocol": protocol,
            "source_ip": src_ip,
            "source_port": src_port,
            "destination_ip": dst_ip,
            "destination_port": dst_port,
            "packet_size": length
        }

        entries.append(entry)

        # Counting
        action_count[action] += 1
        port_count[dst_port] += 1
        ip_count[src_ip] += 1

# Top 3 ports
top_ports = port_count.most_common(3)

# Suspicious IPs (>=3 times)
threats = {ip: count for ip, count in ip_count.items() if count >= 3}

# Save CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Timestamp", "Action", "Protocol", "Source IP", "Source Port",
        "Destination IP", "Destination Port", "Packet Size"
    ])
    for e in entries:
        writer.writerow([
            e["timestamp"], e["action"], e["protocol"],
            e["source_ip"], e["source_port"],
            e["destination_ip"], e["destination_port"],
            e["packet_size"]
        ])

# Save JSON
with open("output.json", "w") as f:
    json.dump(entries, f, indent=4)

# Save threats
with open("threats.txt", "w") as f:
    f.write("THREAT REPORT - Generated: " + str(datetime.now()) + "\n")
    f.write("========================================\n")
    f.write("Suspicious IPs (3+ appearances):\n")
    for ip, count in threats.items():
        f.write(f"IP: {ip} | Occurrences: {count}\n")

# Print report
print("="*60)
print("FIREWALL LOG ANALYSIS REPORT")
print("="*60)
print(f"Total entries processed : {total}")
print(f"Valid entries parsed : {len(entries)}")
print(f"Malformed entries skipped: {malformed}")

print("\n--- Action Summary ---")
for action, count in action_count.items():
    print(f"{action} : {count}")

print("\n--- Top 3 Targeted Destination Ports ---")
for i, (port, count) in enumerate(top_ports, 1):
    print(f"{i}. Port {port} — {count} hits")

print("\n--- Suspicious Source IPs (3+ appearances) ---")
for ip, count in threats.items():
    print(f"{ip} — {count} occurrences")

print("\nOutput saved:")
print("output.csv")
print("output.json")
print("threats.txt")
print("="*60)