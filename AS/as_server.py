# AS/as_server.py

import socket
import threading
import json
import os

DNS_PORT = 53533
RECORDS_FILE = 'records.json'
BUFFER_SIZE = 1024

# Load existing DNS records or initialize an empty dictionary
if os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, 'r') as f:
        dns_records = json.load(f)
else:
    dns_records = {}

def handle_request(data, addr, sock):
    lines = data.decode().strip().split('\n')
    request = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            request[key.strip()] = value.strip()
        else:
            parts = line.split('=')
            if len(parts) == 2:
                key, value = parts
                request[key.strip()] = value.strip()

    if 'TYPE' in request and request['TYPE'] == 'A' and 'NAME' in request:
        name = request['NAME']
        if 'VALUE' in request and 'TTL' in request:
            # Registration request
            value = request['VALUE']
            ttl = request['TTL']
            dns_records[name] = {
                'TYPE': 'A',
                'VALUE': value,
                'TTL': ttl
            }
            with open(RECORDS_FILE, 'w') as f:
                json.dump(dns_records, f)
            print(f"Registered {name} -> {value} with TTL={ttl}")
        else:
            # DNS Query
            if name in dns_records:
                record = dns_records[name]
                response = f"TYPE={record['TYPE']}\nNAME={name}\nVALUE={record['VALUE']}\nTTL={record['TTL']}"
                sock.sendto(response.encode(), addr)
                print(f"Responded to DNS query for {name}")
            else:
                # Record not found; respond with empty response or an error message
                response = f"TYPE=ERROR\nNAME={name}\nERROR=Record not found"
                sock.sendto(response.encode(), addr)
                print(f"Record for {name} not found")

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', DNS_PORT))
    print(f"Authoritative Server is running on UDP port {DNS_PORT}")

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        threading.Thread(target=handle_request, args=(data, addr, sock)).start()

if __name__ == "__main__":
    start_server()
