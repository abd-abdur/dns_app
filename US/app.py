from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

AS_IP = ''
AS_PORT = 53533

def resolve_hostname(hostname):
    message = f"TYPE=A\nNAME={hostname}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (AS_IP, AS_PORT))
    try:
        sock.settimeout(5)
        data, _ = sock.recvfrom(1024)
        response = data.decode().strip().split('\n')
        result = {}
        for line in response:
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
        if 'VALUE' in result:
            return result['VALUE']
        else:
            return None
    except socket.timeout:
        return None
    finally:
        sock.close()

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Validate parameters
    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Update AS details
    global AS_IP, AS_PORT
    AS_IP = as_ip
    AS_PORT = int(as_port)

    # Resolve hostname via AS
    fs_ip = resolve_hostname(hostname)
    if not fs_ip:
        return jsonify({'error': 'Hostname resolution failed'}), 400

    # Query FS for Fibonacci number
    fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    try:
        response = requests.get(fs_url, timeout=5)
        if response.status_code == 200:
            return jsonify({'fibonacci': response.json().get('fibonacci')}), 200
        else:
            return jsonify({'error': 'FS responded with an error'}), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Failed to connect to FS'}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
