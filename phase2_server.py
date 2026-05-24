"""
Phase 2: Symmetric Encryption - SERVER
========================================
Same structure as Phase 1, but now every message is
encrypted with AES-GCM before going on the wire.

What Wireshark will see now:
  - TCP handshake (still visible — that's just connection setup)
  - Then: random-looking binary garbage instead of readable text ✓
"""

import socket
from crypto import send_message, recv_message

HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[SERVER] Listening on {HOST}:{PORT}")
print(f"[SERVER] Using AES-256-GCM encryption")

conn, addr = server_socket.accept()
print(f"[SERVER] Connection from {addr[0]}:{addr[1]}")

# ─── Receive encrypted message ────────────────────────────────────────────────
# recv_message() handles: recv length → recv payload → decrypt → return string
plaintext = recv_message(conn)
print(f"[SERVER] Decrypted message: '{plaintext}'")
print(f"[SERVER] (On the wire this was unreadable ciphertext)")

# ─── Send encrypted reply ─────────────────────────────────────────────────────
reply = "Message received and decrypted successfully. The channel is secure."
send_message(conn, reply)
print(f"[SERVER] Sent encrypted reply")

conn.close()
server_socket.close()
print("[SERVER] Done.")
