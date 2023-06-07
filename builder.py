import tkinter as tk
from tkinter import ttk
import PyInstaller.__main__ as pyinstaller


class BuilderFrame(tk.Frame):
    def __init__(self, root, callback):
        super().__init__(root, width=600, height=400)
        self.callback = callback
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

    def build_client(self):
        host = self.host_entry.get()
        port = self.port_entry.get()
        key = self.key_entry.get()

        # TODO: Use host, port, and key to build the client
        
        # Execute PyInstaller command to build the client
        pyinstaller.run([
            "--onefile",
            "--windowed",
            "--name=Client",
            "client.py"
        ])

        self.callback()

