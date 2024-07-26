from scapy.all import sniff, IP
from flask import Flask, jsonify

app = Flask(__name__)

# This list will store captured packets
packets = []

def packet_callback(packet):
    if packet.haslayer(IP):
        packets.append({
            'timestamp': packet.time,
            'source': packet[IP].src,
            'destination': packet[IP].dst,
            'protocol': packet.proto,
            'info': packet.summary()
        })

def start_capture():
    # Start sniffing packets
    sniff(prn=packet_callback, count=10)  # Adjust count as needed

@app.route('/get-data', methods=['GET'])
def get_data():
    return jsonify(packets)

if __name__ == '__main__':
    start_capture()  # Start capturing packets when server starts
    app.run(debug=True, host='0.0.0.0', port=5000)
