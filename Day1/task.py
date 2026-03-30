# ip_validator.py

def is_valid_ipv4(ip):
    parts = ip.split('.')
    
    if len(parts) != 4:
        return False
    
    for part in parts:
        if not part.isdigit():
            return False
        
        num = int(part)
        
        if num < 0 or num > 255:
            return False
    
    return True


ip_address = input("Enter an IPv4 address: ")

if is_valid_ipv4(ip_address):
    print("Valid IPv4 address.")
else:
    print("Invalid IPv4 address.")