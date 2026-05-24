"""
Phase 1: Raw Sockets - CLIENT
==============================
This is the "dialer" side. It connects to the server,
sends a plaintext message, and receives the reply.

Run this AFTER server.py is already running.
"""

import socket

# ─── Step 1: Create the socket (same as server) ───────────────────────────────
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ─── Step 2: Connect to the server ───────────────────────────────────────────
# This is the key difference from the server — instead of bind+listen+accept,
# the client just CONNECTS to where the server is already waiting.
# This triggers the TCP Three-Way Handshake:
#
#   Client ──── SYN ────────────────► Server   "I want to connect"
#   Client ◄─── SYN-ACK ────────────  Server   "OK, I acknowledge"
#   Client ──── ACK ────────────────► Server   "Great, we're connected"
#
# All of this happens inside .connect() automatically.
HOST = '127.0.0.1'
PORT = 8080

print(f"[CLIENT] Connecting to {HOST}:{PORT}...")
client_socket.connect((HOST, PORT))
print(f"[CLIENT] Connected! (TCP 3-way handshake complete)")

# ─── Step 3: Send a message ──────────────────────────────────────────────────
# This is the message that will appear in PLAINTEXT in Wireshark.
# In later phases, this is what we'll encrypt so Dr. Ganguly can't read it.
message = "Hello from Alice! This is a secret message for Bob."
client_socket.send(message.encode('utf-8'))
print(f"[CLIENT] Sent: '{message}'")
print(f"[CLIENT] ⚠️  This was sent with NO encryption — fully visible on the wire!")

# ─── Step 4: Receive the server's reply ──────────────────────────────────────
raw_reply = client_socket.recv(1024)
reply = raw_reply.decode('utf-8')
print(f"[CLIENT] Received reply: '{reply}'")

# ─── Step 5: Close the connection ────────────────────────────────────────────
client_socket.close()
print("[CLIENT] Connection closed.")
