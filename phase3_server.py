import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
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

# Generate RSA keypair
print("[SERVER] Generating RSA-2048 keypair...")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 8080))
server_socket.listen(1)
print("[SERVER] Listening on 127.0.0.1:8080...")

conn, addr = server_socket.accept()
print(f"[SERVER] Connection from {addr[0]}:{addr[1]}")

# Send public key
pem = public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
send_framed(conn, pem)
print(f"[SERVER] Sent public key ({len(pem)} bytes)")

# Receive encrypted session key
enc_session_key = recv_framed(conn)
session_key = private_key.decrypt(enc_session_key, padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(), label=None))
print(f"[SERVER] Session key decrypted: {session_key.hex()}")
print(f"[SERVER] Handshake complete!")

# Receive and send messages
msg = recv_message(conn, session_key)
print(f"[SERVER] Decrypted message: '{msg}'")

send_message(conn, "Secure channel established. Message received!", session_key)
print("[SERVER] Sent encrypted reply")

conn.close()
server_socket.close()
