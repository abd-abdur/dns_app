# US/app.py

from flask import Flask, request, jsonify, abort
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def user_fibonacci():
    # Extract query parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # Validate parameters
    if not all([hostname, fs_port, number, as_ip, as_port]):
        abort(400, description="Missing one or more required parameters.")

    try:
        fs_port = int(fs_port)
        as_port = int(as_port)
        x = int(number)
    except ValueError:
        abort(400, description="Invalid parameter format. Ports and number must be integers.")

    # Perform DNS query to AS
    dns_query = f"TYPE=A\nNAME={hostname}"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Timeout after 5 seconds
    try:
        sock.sendto(dns_query.encode(), (as_ip, as_port))
        data, _ = sock.recvfrom(1024)
        response = data.decode().strip().split('\n')
        record = {}
        for line in response:
            if '=' in line:
                key, value = line.split('=', 1)
                record[key.strip()] = value.strip()

        if 'TYPE' in record and record['TYPE'] == 'A' and 'VALUE' in record:
            fs_ip = record['VALUE']
        else:
            abort(500, description="Failed to resolve hostname.")
    except socket.timeout:
        abort(500, description="DNS query to AS timed out.")
    except Exception as e:
        abort(500, description=f"DNS query failed: {e}")
    finally:
        sock.close()

    # Send request to FS
    fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={x}"
    try:
        fs_response = requests.get(fs_url, timeout=5)
        if fs_response.status_code == 200:
            fib_number = fs_response.json().get('fibonacci')
            return jsonify({'fibonacci': fib_number}), 200
        else:
            abort(fs_response.status_code, description=fs_response.text)
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Failed to get Fibonacci number from FS: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
