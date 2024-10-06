# FS/app.py

from flask import Flask, request, jsonify, abort
import requests
import socket

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    required_fields = ['hostname', 'ip', 'as_ip', 'as_port']
    if not data or not all(field in data for field in required_fields):
        abort(400, description="Missing required fields.")

    hostname = data['hostname']
    ip_address = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])

    # Create DNS registration message
    dns_message = f"TYPE=A\nNAME={hostname}\nVALUE={ip_address}\nTTL=10"

    # Send UDP message to AS
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(dns_message.encode(), (as_ip, as_port))
        return '', 201
    except Exception as e:
        print(f"Registration failed: {e}")
        abort(500, description="Registration failed.")
    finally:
        sock.close()

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    if number is None:
        abort(400, description="Missing 'number' parameter.")
    try:
        x = int(number)
        fib_number = fibonacci(x)
        return jsonify({'fibonacci': fib_number}), 200
    except ValueError:
        abort(400, description="'number' must be an integer.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
