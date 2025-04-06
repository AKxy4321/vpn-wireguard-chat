# sudo tcpdump -i lo -n udp port 51820 and 'udp[8] = 4' -X

import socket

VPN_IP = "10.0.0.1"  # Server WireGuard IP
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(
    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
)  # Reuse socket incase it was closed abruptly
s.bind((VPN_IP, PORT))
s.listen(1)

print(f"[Server] Listening on {VPN_IP}:{PORT}...")
conn, addr = s.accept()
print(f"[Server] Connection from {addr}")

while True:
    msg = conn.recv(1024).decode()
    if msg.lower() == "exit":
        break
    print(f"[Client]: {msg}")
    reply = input("[You]: ")
    conn.send(reply.encode())

conn.close()
