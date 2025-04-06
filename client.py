# sudo tcpdump -i lo -n tcp port 5555 and "tcp[((tcp[12] & 0xf0) >> 2):1] != 0" -X

import socket

SERVER_IP = "0.0.0.0"  # Server's VPN IP
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))

print(f"[Client] Connected to {SERVER_IP}:{PORT}")

while True:
    msg = input("[You]: ")
    s.send(msg.encode())
    if msg.lower() == "exit":
        break
    reply = s.recv(1024).decode()
    print(f"[Server]: {reply}")

s.close()
