# AS/as_server.py
import socket
import threading
import json
import os

RECORDS_FILE = 'records.json'
UDP_PORT = 53533
BUFFER_SIZE = 1024

# Initialize records file if it doesn't exist
if not os.path.exists(RECORDS_FILE):
    with open(RECORDS_FILE, 'w') as f:
        json.dump({}, f)

def load_records():
    with open(RECORDS_FILE, 'r') as f:
        return json.load(f)

def save_records(records):
    with open(RECORDS_FILE, 'w') as f:
        json.dump(records, f)

def handle_request(data, addr, sock):
    message = data.decode().strip()
    lines = message.split('\n')
    record = {}
    for line in lines:
        parts = line.split('=')
        if len(parts) != 2:
            continue
        key, value = parts
        record[key.strip()] = value.strip()
    
    if 'TYPE' in record and 'NAME' in record:
        if record['TYPE'] == 'A' and 'VALUE' in record:
            # Registration request
            name = record['NAME']
            value = record['VALUE']
            ttl = record.get('TTL', '10')  # Default TTL
            records = load_records()
            records[name] = {
                'TYPE': record['TYPE'],
                'VALUE': value,
                'TTL': ttl
            }
            save_records(records)
            response = f"TYPE={record['TYPE']}\nNAME={name}\nVALUE={value}\nTTL={ttl}\n"
            sock.sendto(response.encode(), addr)
        else:
            # DNS Query
            name = record['NAME']
            records = load_records()
            if name in records:
                rec = records[name]
                response = f"TYPE={rec['TYPE']}\nNAME={name}\nVALUE={rec['VALUE']}\nTTL={rec['TTL']}\n"
            else:
                response = "Error: Record not found.\n"
            sock.sendto(response.encode(), addr)
    else:
        response = "Error: Invalid message format.\n"
        sock.sendto(response.encode(), addr)

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    print(f"Authoritative Server listening on UDP port {UDP_PORT}")
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        threading.Thread(target=handle_request, args=(data, addr, sock)).start()

if __name__ == "__main__":
    start_server()
