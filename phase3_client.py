import socket
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, struct

def recv_exact(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed")
        buf += chunk
    return buf

def send_framed(sock, data):
    sock.sendall(struct.pack('>I', len(data)) + data)

def recv_framed(sock):
    length = struct.unpack('>I', recv_exact(sock, 4))[0]
    return recv_exact(sock, length)

def send_message(sock, plaintext, session_key):
    nonce = os.urandom(12)
    ct = AESGCM(session_key).encrypt(nonce, plaintext.encode(), None)
    payload = nonce + ct
    sock.sendall(struct.pack('>I', len(payload)) + payload)

def recv_message(sock, session_key):
    length = struct.unpack('>I', recv_exact(sock, 4))[0]
    payload = recv_exact(sock, length)
    return AESGCM(session_key).decrypt(payload[:12], payload[12:], None).decode()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("[CLIENT] Connecting to 127.0.0.1:8080...")
client_socket.connect(('127.0.0.1', 8080))
print("[CLIENT] Connected.")

# Receive server public key
pem = recv_framed(client_socket)
public_key = serialization.load_pem_public_key(pem)
print(f"[CLIENT] Received server public key ({len(pem)} bytes)")

# Generate session key and encrypt with server's public key
session_key = os.urandom(32)
enc_session_key = public_key.encrypt(session_key, padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(), label=None))
send_framed(client_socket, enc_session_key)
print(f"[CLIENT] Session key sent (encrypted): {session_key.hex()}")
print(f"[CLIENT] Handshake complete!")

# Send encrypted message
message = "Hello from Alice! This is a secret message for Bob."
send_message(client_socket, message, session_key)
print(f"[CLIENT] Sent encrypted: '{message}'")

reply = recv_message(client_socket, session_key)
print(f"[CLIENT] Decrypted reply: '{reply}'")

client_socket.close()
