import requests
import threading
import ipaddress
import socket
import configparser

threads = []
# Define the path to check
path = '/1600x1200.jpg'
cameraAdresses = []

def check_path_exists(ip, path):
    url = f'http://{ip}{path}'
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            cameraAdresses.append(ip)
            return
    except requests.RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)
        pass
    return

def get_subnet():
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Connect to a non-routable address to determine the local IP address
            s.connect(('69.69.69.69', 1))
            local_ip = s.getsockname()[0]
            ip_parts = local_ip.split(".")
            ip_parts[-1] = "0"
            base_address = ".".join(ip_parts)
            return ipaddress.ip_network(base_address + "/24")
        except Exception:
            local_ip = '127.0.0.1'
    return local_ip

def find_cameras():

    subnet = get_subnet()

# Iterate through each IP in the subnet and check for the path
    for ip in subnet:
        threads.append(threading.Thread(target=check_path_exists, args=(ip,path)))
        threads[-1].start()

    for thread in threads:
        thread.join()
    
    print(f"Found {len(cameraAdresses)} cameras: {cameraAdresses}")
    # Write cameraAdresses to config.ini
    if len(cameraAdresses) == 2:
        config = configparser.ConfigParser()
        config.read("Backend/config.ini")
        config["CAMERA"]["URL_LEFT"] = str(cameraAdresses[0])
        config["CAMERA"]["URL_RIGHT"] = str(cameraAdresses[1])
        with open("Backend/config.ini", "w") as configFile:
            config.write(configFile)

    return
