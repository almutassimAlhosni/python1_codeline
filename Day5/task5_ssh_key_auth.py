import paramiko
import os

host = "192.168.100.41"
username = "ssh almutassim@ 192.168.100.41"
key_path = os.path.expanduser("~/.ssh/id_rsa_paramiko")

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=host, username=username, key_filename=key_path)

    stdin, stdout, stderr = ssh.exec_command("ls")

    print("OUTPUT:")
    print(stdout.read().decode())

    print("ERROR:")
    print(stderr.read().decode())

    ssh.close()

except Exception as e:
    print("Connection failed:")
    print(e)