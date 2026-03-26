from flask import Flask, jsonify, request, render_template
import socket
from discover import getActiveSSHDevices, getDeviceData

app = Flask(__name__)

DEFAULT_SUBNET = "192.168.1.0/24"
cached_devices = {} 

def preload_network(subnet):
    print(f"Preloading network on {subnet}... (This might take a moment)")
    found_ips = getActiveSSHDevices(subnet)
    
    for ip in found_ips:
        device_data = getDeviceData(ip, "admin", "cisco") 
        if device_data:
            device_data["ip"] = ip
            cached_devices[ip] = device_data
            print(f"Preloaded data for {ip}")
    
    print("Preloading complete! App is ready.")

preload_network(DEFAULT_SUBNET)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_devices", methods=["GET"])
def get_devices():
    return jsonify({"devices": list(cached_devices.values())})

@app.route("/check_ip", methods=["POST"])
def check_ip():
    data = request.get_json()
    ip = data.get("ip")
    
    if not ip:
        return jsonify({"error": "No IP provided"}), 400
        
    if ip in cached_devices:
        return jsonify({"message": "IP already in cache", "device": cached_devices[ip]})
        
    print(f"Checking new IP: {ip}...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    is_open = sock.connect_ex((str(ip), 22)) == 0
    sock.close()
    
    if is_open:
        print(f"New SSH device found at {ip}. Fetching data...")
        device_data = getDeviceData(ip, "admin", "cisco")
        if device_data:
            device_data["ip"] = ip
            cached_devices[ip] = device_data
            return jsonify({"message": "New device found and added", "device": device_data})
    
    return jsonify({"message": "No active SSH device found at this IP", "device": None}), 404

@app.route("/run_discovery", methods=["POST"])
def run_discovery():
    data = request.get_json()
    subnet = data.get("subnet", DEFAULT_SUBNET)
    
    print(f"Starting manual full scan on {subnet}...")
    
    found_ips = getActiveSSHDevices(subnet)
    
    for ip in found_ips:
        if ip not in cached_devices:
            device_data = getDeviceData(ip, "admin", "cisco")
            if device_data:
                device_data["ip"] = ip
                cached_devices[ip] = device_data

    return jsonify({"devices": list(cached_devices.values())})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)