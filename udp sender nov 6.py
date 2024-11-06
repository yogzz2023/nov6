import socket
import time
import random

def send_measurements():
    udp_ip = "127.0.0.1"
    udp_port = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        # Generate random measurement data
        mr = random.uniform(0, 1000)
        ma = random.uniform(0, 360)
        me = random.uniform(-90, 90)
        mt = time.time()
        md = random.uniform(-50, 50)
        message = f"{mr},{ma},{me},{mt},{md}"
        
        sock.sendto(message.encode(), (udp_ip, udp_port))
        time.sleep(1)  # Send a measurement every second

if __name__ == "__main__":
    send_measurements()
