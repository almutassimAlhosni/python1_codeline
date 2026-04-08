import paramiko

# Replace with your details
hostname = "your_device_ip"
username = "your_username"
key_path = r"C:\Users\YourName\.ssh\id_rsa_paramiko"  # Windows path

def main():
    try:
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)

        # Connect using SSH key (no password)
        client.connect(hostname=hostname, username=username, pkey=private_key)

        print("✅ Connected successfully using SSH key!")

        # Run a command
        stdin, stdout, stderr = client.exec_command("whoami")

        print("\nOutput:")
        print(stdout.read().decode())

        # Close connection
        client.close()

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()