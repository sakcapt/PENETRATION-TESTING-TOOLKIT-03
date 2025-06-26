# Penetration Testing Toolkit

import socket
import threading
import paramiko

# Module 1: Port Scanner
def port_scanner(target, ports):
    print(f"Scanning target: {target}")
    for port in ports:
        threading.Thread(target=scan_port, args=(target, port)).start()


def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} is open on {target}.")
        s.close()
    except Exception as e:
        print(f"[-] Error scanning port {port}: {e}")


# Module 2: Brute-Forcer
def ssh_brute_force(host, username, password_list):
    print(f"Starting SSH brute force on {host} with username {username}.")
    for password in password_list:
        if try_ssh_login(host, username, password):
            print(f"[+] Login successful! Username: {username}, Password: {password}")
            return True
        else:
            print(f"[-] Failed attempt with password: {password}")
    return False


def try_ssh_login(host, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        print(f"[-] Error during SSH login: {e}")
        return False


# Main Menu
def main():
    print("Penetration Testing Toolkit")
    print("1. Port Scanner")
    print("2. SSH Brute-Forcer")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        target = input("Enter target IP address: ")
        ports = input("Enter ports to scan (comma-separated): ").split(",")
        ports = [int(port.strip()) for port in ports]
        port_scanner(target, ports)

    elif choice == "2":
        host = input("Enter target IP address: ")
        username = input("Enter username: ")
        password_file = input("Enter path to password file: ")
        try:
            with open(password_file, 'r') as file:
                password_list = [line.strip() for line in file.readlines()]
            ssh_brute_force(host, username, password_list)
        except FileNotFoundError:
            print("Password file not found.")

    elif choice == "3":
        print("Exiting toolkit.")

    else:
        print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
