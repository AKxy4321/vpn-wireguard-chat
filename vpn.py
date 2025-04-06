import os
import subprocess


def generate_keys():
    """Generate WireGuard private and public keys for server and client, if not already present."""
    os.makedirs("wg_keys", exist_ok=True)

    # Generate server keys
    if not (
        os.path.exists("wg_keys/server_privatekey")
        and os.path.exists("wg_keys/server_publickey")
    ):
        print("🔑 Generating server keys...")
        subprocess.run(
            "wg genkey | tee wg_keys/server_privatekey | wg pubkey > wg_keys/server_publickey",
            shell=True,
            check=True,
        )
    else:
        print("✅ Server keys already exist, skipping generation.")

    # Generate client keys
    if not (
        os.path.exists("wg_keys/client_privatekey")
        and os.path.exists("wg_keys/client_publickey")
    ):
        print("🔑 Generating client keys...")
        subprocess.run(
            "wg genkey | tee wg_keys/client_privatekey | wg pubkey > wg_keys/client_publickey",
            shell=True,
            check=True,
        )
    else:
        print("✅ Client keys already exist, skipping generation.")


def create_config():
    """Create WireGuard server and client configuration files."""
    with open("wg_keys/server_privatekey") as f:
        server_priv = f.read().strip()
    with open("wg_keys/server_publickey") as f:
        server_pub = f.read().strip()
    with open("wg_keys/client_privatekey") as f:
        client_priv = f.read().strip()
    with open("wg_keys/client_publickey") as f:
        client_pub = f.read().strip()

    network_interface = "wlp3s0"  # Change to your actual external network interface

    # Server config - wg0
    server_config = f"""
[Interface]
PrivateKey = {server_priv}
Address = 10.0.0.1/24
ListenPort = 51820
SaveConfig = true
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o {network_interface} -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o {network_interface} -j MASQUERADE

[Peer]
PublicKey = {client_pub}
AllowedIPs = 10.0.0.2/32
PersistentKeepalive = 25
"""

    # Client config - wg1
    client_config = f"""
[Interface]
PrivateKey = {client_priv}
Address = 10.0.0.2/24

[Peer]
PublicKey = {server_pub}
Endpoint = 127.0.0.1:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

    os.makedirs("/etc/wireguard", exist_ok=True)

    with open("/etc/wireguard/wg0.conf", "w") as f:
        f.write(server_config.strip())

    with open("/etc/wireguard/wg1.conf", "w") as f:
        f.write(client_config.strip())

    print("✅ Server (wg0) and Client (wg1) config files created.")


def start_vpn():
    """Start both the WireGuard server and client."""
    print("🚀 Starting server (wg0)...")
    subprocess.run("wg-quick up wg0", shell=True, check=True)
    print("🚀 Starting client (wg1)...")
    subprocess.run("wg-quick up wg1", shell=True, check=True)


def stop_vpn():
    """Stop both the WireGuard server and client, then delete config files."""
    print("🛑 Stopping client (wg1)...")
    subprocess.run("wg-quick down wg1", shell=True, check=True)

    print("🛑 Stopping server (wg0)...")
    subprocess.run("wg-quick down wg0", shell=True, check=True)

    # Delete configuration files
    try:
        os.remove("/etc/wireguard/wg0.conf")
        print("🧹 Deleted /etc/wireguard/wg0.conf")
    except FileNotFoundError:
        print("⚠️ /etc/wireguard/wg0.conf not found.")

    try:
        os.remove("/etc/wireguard/wg1.conf")
        print("🧹 Deleted /etc/wireguard/wg1.conf")
    except FileNotFoundError:
        print("⚠️ /etc/wireguard/wg1.conf not found.")


def show_status():
    """Show WireGuard VPN status."""
    subprocess.run("wg show", shell=True, check=True)


def main():
    generate_keys()
    create_config()
    start_vpn()
    show_status()
    print("\n✅ VPN started successfully (Server: wg0, Client: wg1)")
    stop = input("Enter 'STOP' when you want to close the VPN: ")
    if stop.strip().upper() == "STOP":
        stop_vpn()


if __name__ == "__main__":
    main()
