Here's your updated **README** with the inclusion of both the normal (unencrypted) TCP chat and the VPN-based TCP chat (`server_vpn.py` and `client_vpn.py`). The README now compares both approaches and clearly states their usage.

---

# WireGuard VPN Setup & Encrypted TCP Chat (Python)

## 🛡️ Overview

This project sets up a secure WireGuard-based VPN using Python automation, and demonstrates **end-to-end encrypted communication** using a simple TCP server and client over the VPN tunnel. It also includes a **normal, unencrypted TCP chat** for comparison.

It's designed for **local testing**, with both the server and client running on the same machine, communicating securely via the WireGuard interface.

---

## 🚀 Features

- ✅ Automatic generation of WireGuard keys (if not already present)
- ✅ Auto-creation of `wg0` (server) and `wg1` (client) configuration files
- ✅ Auto-start/stop of the VPN interfaces
- ✅ Encrypted TCP chat between VPN server and client (`server_vpn.py` + `client_vpn.py`)
- ✅ Normal (unencrypted) TCP chat (`server_normal.py` + `client_normal.py`)
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

### 1. Python Script (`vpn.py`)
This script:

- Generates server/client keys
- Creates `/etc/wireguard/wg0.conf` (server) and `/etc/wireguard/wg1.conf` (client)
- Starts both interfaces
- Displays VPN status
- Waits for user input (`STOP`) to shut down the VPN and clean up configs

### 2. Chat Applications

#### 🟢 Encrypted Chat over VPN:
- `server_vpn.py`: Listens on `10.0.0.1:5555` (VPN interface)
- `client_vpn.py`: Connects to `10.0.0.1:5555` via VPN tunnel

#### 🔵 Normal Unencrypted Chat (No VPN):
- `server_normal.py`: Listens on `0.0.0.0:5555` (normal interface)
- `client_normal.py`: Connects to `0.0.0.0:5555` via default route

---

## 📁 Project Structure

```
.
├── vpn.py              # Automates WireGuard VPN setup
├── server_vpn.py        # TCP chat server over VPN
├── client_vpn.py        # TCP chat client over VPN
├── server_normal.py     # Normal TCP server (no VPN)
├── client_normal.py     # Normal TCP client (no VPN)
├── wg_keys/             # Generated private/public key files
```

---

## ⚙️ Usage

### Step 1: Run the VPN Setup
```bash
sudo python vpn.py
```

> You'll see keys generated, configs created, and both `wg0` and `wg1` interfaces brought up.

Once started, the script waits for you to type `STOP` to shut down and clean everything.

---

### Step 2: Run the Chat Apps in Separate Terminals

#### 🔵 For Normal Chat (No VPN)
**Terminal A:**
```bash
sudo python server.py
```
**Terminal B:**
```bash
sudo python client.py
```

#### 🟢 For VPN-Encrypted Chat (Run VPN before attempting)
**Terminal A:**
```bash
sudo python server_vpn.py
```
**Terminal B:**
```bash
sudo python client_vpn.py
```

Now you can compare both types of communication! 🎉

---

### Step 3: Tear Down the VPN

In the `vpn.py` terminal, type:
```text
STOP
```

This stops both interfaces and deletes the config files.

---

## 🧪 Packet Sniffing (Debug)

To monitor WireGuard handshake and traffic:
```bash
sudo tcpdump -i lo -n udp port 51820 and 'udp[8] = 4' -X
```

To monitor unencrypted TCP messages (normal chat):
```bash
sudo tcpdump -i lo -n tcp port 5555 and "tcp[((tcp[12] & 0xf0) >> 2):1] != 0" -X
```

---

## 🧯 Troubleshooting

- **VPN not working?**
  - Make sure your network interface in `vpn.py` is correct (e.g., `wlp3s0`, `eth0`, etc.)
  - Run `sudo wg show` to check for active connections

- **Permission errors?**
  - Always run scripts with `sudo`, especially those that modify `/etc/wireguard` or start network interfaces

---

## ✅ Conclusion

You now have a complete setup for:

- ✅ Creating a local VPN using WireGuard
- ✅ Running secure encrypted chat over that VPN
- ✅ Comparing it with a normal, unsecured TCP chat

Great for learning networking, security, and VPN internals in a hands-on way! 🚀

---

Would you also like a matching project description and topics for GitHub (`README.md`, `description`, and tags)?