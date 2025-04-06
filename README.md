---

# WireGuard VPN Setup & Encrypted TCP Chat (Python)

## 🛡️ Overview

This project sets up a secure WireGuard-based VPN using Python automation, and demonstrates end-to-end encrypted communication using a simple TCP server and client. It's designed for **local testing**, with both the server and client running on the same machine over the VPN tunnel.

---

## 🚀 Features

- ✅ Automatic generation of WireGuard keys (if not already present)
- ✅ Auto-creation of `wg0` (server) and `wg1` (client) configuration files
- ✅ Auto-start/stop of the VPN interfaces
- ✅ Simple TCP-based chat between VPN server and client (Python sockets)
- ✅ Run both ends on the same machine for testing

---

## 🛠️ Prerequisites

- **Linux system** (tested on Arch Linux)
- `wireguard-tools` installed
- `iptables` installed
- Python 3.x

### 📦 Install Required Packages
```bash
sudo pacman -S wireguard-tools iptables  # Arch
# OR
sudo apt install wireguard iptables      # Debian/Ubuntu
```

---

## 🔧 How It Works

### 1. Python Script (`main.py`)
This script:

- Generates server/client keys
- Creates `/etc/wireguard/wg0.conf` (server) and `wg1.conf` (client)
- Starts both interfaces
- Displays VPN status
- Waits for user input to stop VPN and clean up configs

### 2. Chat Server & Client

- `server.py`: Binds to VPN IP `10.0.0.1`, listens on TCP port `5555`
- `client.py`: Connects to `10.0.0.1:5555` over the VPN tunnel

---

## 📁 Project Structure

```
.
├── main.py           # Automates WireGuard VPN setup
├── server.py         # TCP chat server (VPN endpoint)
├── client.py         # TCP chat client
├── wg_keys/          # Generated private/public key files
```

---

## ⚙️ Usage

### Step 1: Run the VPN Setup
```bash
sudo python main.py
```

> You'll see keys generated, configs created, and both `wg0` and `wg1` brought up.

Once started, the script waits for you to type `STOP` to shut down and clean everything.

---

### Step 2: Run the TCP Chat (Different Terminals)

**Terminal A: Run the server**
```bash
sudo python server_vpn.py
```

**Terminal B: Run the client**
```bash
sudo python client_vpn.py
```

Now you can chat securely via the VPN tunnel! 🎉

---

### Step 3: Tear Down the VPN

In the `main.py` terminal, type:
```text
STOP
```

This brings down both interfaces and deletes the config files.

---

## 🧪 Packet Sniffing (Debug)

To sniff WireGuard packets (UDP port 51820):
```bash
sudo tcpdump -i lo -n udp port 51820 and 'udp[8] = 4' -X
```

---

## 🧯 Troubleshooting

- **VPN not working?**
  - Make sure your network interface in `main.py` is correct (e.g., `wlp3s0`, `eth0`, etc.).
  - Check `sudo wg show` for active sessions.

- **Permission errors?**
  - Run everything with `sudo`, especially when writing to `/etc/wireguard` or starting interfaces.

---

## ✅ Conclusion

You now have a fully working WireGuard VPN setup **with automation and encrypted TCP messaging over the VPN tunnel** — all running locally for safe testing and learning!

---