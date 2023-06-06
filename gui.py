import tkinter as tk
from tkinter import ttk
import threading
import os
import socket
from builder import BuilderFrame


class ControlCommandCenterGUI:
    def __init__(self, root):
        self.root = root

        self.create_gui()

        # Example client data
        self.clients = [
            {"client_id": "Client1", "ip_address": "192.168.1.10", "status": "Connected"},
            {"client_id": "Client2", "ip_address": "192.168.1.20", "status": "Connected"},
            {"client_id": "Client3", "ip_address": "192.168.1.30", "status": "Connected"}
        ]
        self.update_client_list()

    def create_gui(self):
        # Side panel
        self.side_panel = tk.Frame(self.root, width=200, bg="lightgray")
        self.side_panel.pack(side="left", fill="y")

        # Client List button
        client_list_button = ttk.Button(self.side_panel, text="Client List", command=self.show_client_list)
        client_list_button.pack(pady=10)

        # Options in the side panel
        options = ["Builder", "Binder", "Crypter", "Spreader", "Updater", "Social", "Downloader", "Binaries", "Miner"]
        for option in options:
            btn = ttk.Button(self.side_panel, text=option, command=lambda opt=option: self.option_selected(opt))
            btn.pack(pady=10)

        # Client list view
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("IP", "Status")
        self.tree.heading("#0", text="Client ID")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)

        # Ping clients button
        ping_button = ttk.Button(self.side_panel, text="Ping Clients", command=self.ping_clients)
        ping_button.pack(pady=10)

    def update_client_list(self):
        # Clear existing items in the tree
        self.tree.delete(*self.tree.get_children())

        # Insert updated client list into the tree
        for client in self.clients:
            client_id = client["client_id"]
            ip_address = client["ip_address"]
            status = client["status"]
            self.tree.insert("", "end", text=client_id, values=(ip_address, status))

    def option_selected(self, option):
        if option == "Builder":
            self.show_builder_frame()

    def show_builder_frame(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.pack_forget()

    # Builder frame
        builder_frame = BuilderFrame(self.root, self.builder_callback, self)
        builder_frame.pack()


    def builder_callback(self, host, port, key):
        # Placeholder function to handle client build process
        print("Building client...")
        print("Host:", host)
        print("Port:", port)
        print("Encryption Key:", key)

        # After building the client, return to the main GUI
        self.create_gui()
        self.update_client_list()

    def ping_clients(self):
        # Ping all clients to get a status update
        for client in self.clients:
            ip_address = client["ip_address"]
            threading.Thread(target=self.ping_client, args=(ip_address,), daemon=True).start()

    def ping_client(self, ip_address):
        # Ping a client and update its status
        try:
            socket.setdefaulttimeout(5)
            response = os.system("ping -n 1 " + ip_address)
            if response == 0:
                self.update_client_status(ip_address, "Connected")
            else:
                self.update_client_status(ip_address, "Disconnected")
        except:
            self.update_client_status(ip_address, "Disconnected")

    def update_client_status(self, ip_address, status):
        # Update the status of a client in the list
        for client in self.clients:
            if client["ip_address"] == ip_address:
                client["status"] = status
                break

        # Update the client list view
        self.update_client_list()

    def show_client_list(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Re-create the GUI
        self.create_gui()
        self.update_client_list()
