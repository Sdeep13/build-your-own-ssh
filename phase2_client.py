"""
Phase 2: Symmetric Encryption - CLIENT
========================================
Same structure as Phase 1, but messages are encrypted
before sending and decrypted after receiving.
"""

import socket
from crypto import send_message, recv_message

HOST = '127.0.0.1'
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[CLIENT] Connecting to {HOST}:{PORT}...")
client_socket.connect((HOST, PORT))
print(f"[CLIENT] Connected.")

# ─── Send encrypted message ───────────────────────────────────────────────────
message = "Hello from Alice! This is a secret message for Bob."
send_message(client_socket, message)
print(f"[CLIENT] Sent (encrypted): '{message}'")
print(f"[CLIENT] On the wire: [nonce][AES-GCM ciphertext][auth tag] — all binary garbage")

# ─── Receive encrypted reply ──────────────────────────────────────────────────
reply = recv_message(client_socket)
print(f"[CLIENT] Decrypted reply: '{reply}'")

client_socket.close()
print("[CLIENT] Done.")
