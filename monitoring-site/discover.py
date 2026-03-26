import socket
import ipaddress
from netmiko import ConnectHandler

def getActiveSSHDevices(subnet):
    network = ipaddress.ip_network(subnet, strict=False)
    
    hosts = list(network.hosts())
    found = []

    for index, ip in enumerate(hosts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        
        if sock.connect_ex((str(ip), 22)) == 0:
            found.append(str(ip))
            
        sock.close()

    return found


def getDeviceData(ip, username="admin", password="cisco", secret="cisco"):
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": username,
        "password": password,
        "secret": secret,
    }
    
    try:
        connection = ConnectHandler(**device)
        
        if not connection.check_enable_mode():
            connection.enable()
            print(f"[{ip}] Entered privileged EXEC mode.")
        
        hostname_out = connection.send_command("show running-config | include hostname")
        hostname = hostname_out.replace("hostname ", "").strip()
        
        ospf_out = connection.send_command("show ip ospf neighbor")
        stp_out = connection.send_command("show spanning-tree")
        vlan_out = connection.send_command("show vlan brief")
        port_sec_out = connection.send_command("show port-security")
        config_out = connection.send_command("show running-config")
        
        connection.disconnect()
        
        interfaces = []
        current_interface = None
        
        for line in config_out.splitlines():
            if line.startswith("interface "):
                if current_interface:
                    interfaces.append(current_interface)
                
                current_interface = {
                    "name": line.replace("interface ", "").strip(),
                    "ip": "Unassigned",
                    "status": "Up" 
                }
                
            elif current_interface and line.startswith(" ip address "):
                parts = line.strip().split()
                if len(parts) >= 3 and parts[1] == "address":
                    current_interface["ip"] = parts[2]
                    
            elif current_interface and line.strip() == "shutdown":
                current_interface["status"] = "Shutdown"
                
            elif current_interface and line.startswith("!"):
                interfaces.append(current_interface)
                current_interface = None
                
        if current_interface:
            interfaces.append(current_interface)

        return {
            "hostname": hostname,
            "interfaces": interfaces,
            "ospf": ospf_out,
            "stp": stp_out,
            "vlans": vlan_out,
            "port_security": port_sec_out,
            "run_conf": config_out
        }
        
    except Exception as e:
        print(f"Error connecting to {ip}: {e}")
        return None