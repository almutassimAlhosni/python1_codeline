
while True:
        
    ip = input("Enter IP address: ")
    cidr = input("Enter CIDR prefix (e.g., 24): ")
    import ipaddress

    # use TRY & EXPECT for invalid input
    try:
        network = ipaddress.ip_network(ip + "/" + cidr, strict=False)

        print("--- Subnet Calculator ---")
        print("Network Address:", network.network_address)
        print("Broadcast Address:", network.broadcast_address)
        print("Number of Usable Hosts:", network.num_addresses - 2)

    except ValueError as e:
        print("--- Subnet Calculator ---")
        print("Error: Invalid IP address or CIDR prefix provided. Details:", e)
        print("-------------------------")