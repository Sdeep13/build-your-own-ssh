"""
Phase 1: Raw Sockets - SERVER
==============================
This is the "listener" side. It waits for a client to connect,
receives a plaintext message, and sends a reply.

Run this FIRST, then run client.py in another terminal.
"""

import socket  # Python's built-in socket library — wraps OS-level TCP sockets

# ─── Step 1: Create the socket ───────────────────────────────────────────────
# socket.AF_INET     → use IPv4 addresses (e.g. 127.0.0.1)
# socket.SOCK_STREAM → use TCP (stream-based, reliable, ordered)
#                      (SOCK_DGRAM would be UDP — unreliable, no connection)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ─── Step 2: Set socket option ───────────────────────────────────────────────
# SO_REUSEADDR lets us reuse the port immediately after the program exits.
# Without this, you'd get "Address already in use" if you restart quickly.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# ─── Step 3: Bind to an address and port ─────────────────────────────────────
# '127.0.0.1' = localhost (only reachable from this same machine)
# 8080        = port number (like an apartment number within the building/IP)
# Ports 0-1023 are "well-known" (reserved for HTTP=80, SSH=22, etc.)
# We use 8080 to stay out of that reserved range.
HOST = '127.0.0.1'
PORT = 8080

server_socket.bind((HOST, PORT))
print(f"[SERVER] Socket bound to {HOST}:{PORT}")

# ─── Step 4: Start listening ──────────────────────────────────────────────────
# backlog=1 means: queue at most 1 unaccepted connection before refusing others.
# Think of it as: "I can handle 1 person waiting outside my door."
server_socket.listen(1)
print(f"[SERVER] Listening for connections...")

# ─── Step 5: Accept a connection ─────────────────────────────────────────────
# .accept() BLOCKS here — the program pauses and waits until a client connects.
# It returns:
#   conn → a NEW socket object for this specific client conversation
#   addr → the client's (IP, port) tuple
conn, addr = server_socket.accept()
print(f"[SERVER] Connection accepted from {addr[0]}:{addr[1]}")

# ─── Step 6: Receive data ────────────────────────────────────────────────────
# .recv(1024) → receive up to 1024 bytes
# TCP is a STREAM protocol — there are no message boundaries.
# In real code you'd loop until you get a complete message.
# For now, one recv() is enough for our short message.
raw_data = conn.recv(1024)

# Data arrives as bytes. Decode to a Python string using UTF-8.
message = raw_data.decode('utf-8')
print(f"[SERVER] Received: '{message}'")
print(f"[SERVER] ⚠️  Notice: this message was sent in PLAINTEXT!")
print(f"[SERVER]    Anyone sniffing the network (like Wireshark) can read it.")

# ─── Step 7: Send a reply ────────────────────────────────────────────────────
# Must encode the string back to bytes before sending.
reply = "Hello from server! I got your message."
conn.send(reply.encode('utf-8'))
print(f"[SERVER] Sent reply: '{reply}'")

# ─── Step 8: Close connections ───────────────────────────────────────────────
conn.close()           # close this client's connection
server_socket.close()  # close the listening socket
print("[SERVER] Connection closed.")
