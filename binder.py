import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess

class BinderFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=600, height=400)
        self.pack_propagate(0)
        self.create_widgets()
        self.selected_files = {}  # Dictionary to store selected files for each button
        self.load_order = []  # List to store the load order of the selected files
        self.selected_directory = None  # Variable to store selected output directory

    def create_widgets(self):
        label = ttk.Label(self, text="This is the Binder Frame")
        label.pack()

        select_file_button_1 = ttk.Button(self, text="Select File 1", command=lambda: self.select_file(1))
        select_file_button_1.pack()

        file_label_1 = ttk.Label(self, text="")
        file_label_1.pack()
        self.file_labels = [file_label_1]  # List to store file labels for each button

        select_file_button_2 = ttk.Button(self, text="Select File 2", command=lambda: self.select_file(2))
        select_file_button_2.pack()

        file_label_2 = ttk.Label(self, text="")
        file_label_2.pack()
        self.file_labels.append(file_label_2)

        load_order_frame = ttk.Frame(self)
        load_order_frame.pack()

        load_order_label = ttk.Label(load_order_frame, text="Load Order:")
        load_order_label.grid(row=0, column=0, sticky=tk.W)

        self.load_order_tree = ttk.Treeview(load_order_frame, selectmode="browse")
        self.load_order_tree.grid(row=1, column=0)

        up_button = ttk.Button(load_order_frame, text="Up", command=self.move_up)
        up_button.grid(row=1, column=1, padx=5)

        down_button = ttk.Button(load_order_frame, text="Down", command=self.move_down)
        down_button.grid(row=1, column=2, padx=5)

        directory_button = ttk.Button(self, text="Select Output Directory", command=self.select_directory)
        directory_button.pack()

        directory_label = ttk.Label(self, text="")
        directory_label.pack()
        self.directory_label = directory_label

        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack()

    def select_file(self, button_index):
        file_path = filedialog.askopenfilename(title=f"Select File {button_index}", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if file_path:
            self.selected_files[button_index] = file_path
            self.file_labels[button_index - 1]["text"] = file_path

            # Update load order tree with selected files
            self.update_load_order_tree()

    def update_load_order_tree(self):
        self.load_order_tree.delete(*self.load_order_tree.get_children())

        for index, file_path in enumerate(self.load_order, start=1):
            self.load_order_tree.insert("", "end", text=f"File {index}", values=(file_path,))

    def move_up(self):
        selected_item = self.load_order_tree.selection()
        if selected_item:
            index = self.load_order.index(selected_item[0])
            if index > 0:
                self.load_order.remove(selected_item[0])
                self.load_order.insert(index - 1, selected_item[0])
                self.update_load_order_tree()

    def move_down(self):
        selected_item = self.load_order_tree.selection()
        if selected_item:
            index = self.load_order.index(selected_item[0])
            if index < len(self.load_order) - 1:
                self.load_order.remove(selected_item[0])
                self.load_order.insert(index + 1, selected_item[0])
                self.update_load_order_tree()

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.selected_directory = directory
            self.directory_label["text"] = directory

    def join_files(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected.")
            return

        if not self.load_order:
            messagebox.showerror("Error", "No load order selected.")
            return

        if not self.selected_directory:
            messagebox.showerror("Error", "No output directory selected.")
            return

        # Join files into a single executable using the selected load order
        output_file = filedialog.asksaveasfilename(
            title="Save As", defaultextension=".exe",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if not output_file:
            return

        # Build the join command based on the selected tool
        tool = "IExpress"  # Default to IExpress if no tool is selected
        if self.use_makeself.get():
            tool = "makeself"

        command = ""
        if tool == "IExpress":
            command = self.build_iexpress_command(output_file)
        elif tool == "makeself":
            command = self.build_makeself_command(output_file)

        if command:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                messagebox.showerror("Error", f"Joining process failed:\n{stderr.decode('utf-8')}")
            else:
                messagebox.showinfo("Success", f"Joining process completed.\nOutput file: {output_file}")

    def build_iexpress_command(self, output_file):
        # Create the IExpress configuration file
        config_file_content = f"""[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=ExtractOnly
ShowInstallProgramWindow=0
HideExtractAnimation=1
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName={os.path.basename(output_file)}
[Tasks]
[Files]"""

        # Add the selected files to the configuration file
        for file_path in self.load_order:
            config_file_content += f"\n\"{file_path}\""

        # Write the configuration file to disk
        config_file_path = os.path.join(self.selected_directory, "config.txt")
        with open(config_file_path, "w") as config_file:
            config_file.write(config_file_content)

        # Create a temporary batch file to run the IExpress command
        batch_file_content = f"""@echo off
IExpress /N /Q {config_file_path}
del /F {config_file_path}
"""
        batch_file_path = os.path.join(self.selected_directory, "join.bat")
        with open(batch_file_path, "w") as batch_file:
            batch_file.write(batch_file_content)

        return [batch_file_path]

    def build_makeself_command(self, output_file):
        # Build the makeself command
        command = [
            "makeself.sh", "--gzip", "--nocomp", "--notemp", "--nocrc",
            self.selected_directory, output_file, "Join Files", *self.load_order
        ]

        return command
