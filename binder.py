import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os


class BinderFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selected_files = []
        self.load_order = []
        self.selected_directory = ""

        # Create UI elements
        self.create_file_selection()
        self.create_load_order()
        self.create_output_directory()

        # Create Join button
        self.join_button = ttk.Button(
            self, text="Join Files", command=self.join_files
        )
        self.join_button.pack(side=tk.BOTTOM, pady=10)

    def create_file_selection(self):
        file_selection_frame = ttk.Frame(self)
        file_selection_frame.pack(side=tk.LEFT, padx=10)

        # Create Select File 1 button and display box
        self.file1_path = tk.StringVar()
        select_file1_button = ttk.Button(
            file_selection_frame, text="Select File 1", command=self.select_file1
        )
        select_file1_button.pack(side=tk.TOP, pady=5)
        file1_display = ttk.Entry(
            file_selection_frame, textvariable=self.file1_path, width=50, state="readonly"
        )
        file1_display.pack(side=tk.TOP, pady=5)

        # Create Select File 2 button and display box
        self.file2_path = tk.StringVar()
        select_file2_button = ttk.Button(
            file_selection_frame, text="Select File 2", command=self.select_file2
        )
        select_file2_button.pack(side=tk.TOP, pady=5)
        file2_display = ttk.Entry(
            file_selection_frame, textvariable=self.file2_path, width=50, state="readonly"
        )
        file2_display.pack(side=tk.TOP, pady=5)

    def create_load_order(self):
        load_order_frame = ttk.Frame(self)
        load_order_frame.pack(side=tk.LEFT, padx=10)

        # Create Load Order label
        load_order_label = ttk.Label(load_order_frame, text="Load Order")
        load_order_label.pack(side=tk.TOP)

        # Create Load Order listbox
        self.load_order_listbox = tk.Listbox(load_order_frame, selectmode=tk.SINGLE, width=50)
        self.load_order_listbox.pack(side=tk.TOP, pady=5)

        # Create Up and Down buttons for load order
        up_button = ttk.Button(load_order_frame, text="Up", command=self.move_up)
        up_button.pack(side=tk.TOP)
        down_button = ttk.Button(load_order_frame, text="Down", command=self.move_down)
        down_button.pack(side=tk.TOP)

    def create_output_directory(self):
        output_directory_frame = ttk.Frame(self)
        output_directory_frame.pack(side=tk.LEFT, padx=10)

        # Create Select Output Directory button and display box
        self.directory_path = tk.StringVar()
        select_directory_button = ttk.Button(
            output_directory_frame, text="Select Output Directory", command=self.select_directory
        )
        select_directory_button.pack(side=tk.TOP, pady=5)
        directory_display = ttk.Entry(
            output_directory_frame, textvariable=self.directory_path, width=50, state="readonly"
        )
        directory_display.pack(side=tk.TOP, pady=5)

    def select_file1(self):
        file_path = filedialog.askopenfilename(title="Select File 1")
        if file_path:
            self.file1_path.set(file_path)

    def select_file2(self):
        file_path = filedialog.askopenfilename(title="Select File 2")
        if file_path:
            self.file2_path.set(file_path)

    def move_up(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:
                self.load_order_listbox.delete(index)
                self.load_order_listbox.insert(index - 1, self.load_order[index])
                self.load_order[index], self.load_order[index - 1] = (
                    self.load_order[index - 1],
                    self.load_order[index],
                )
                self.load_order_listbox.selection_set(index - 1)

    def move_down(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.load_order) - 1:
                self.load_order_listbox.delete(index)
                self.load_order_listbox.insert(index + 1, self.load_order[index])
                self.load_order[index], self.load_order[index + 1] = (
                    self.load_order[index + 1],
                    self.load_order[index],
                )
                self.load_order_listbox.selection_set(index + 1)

    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.directory_path.set(directory)
            self.selected_directory = directory

    def join_files(self):
        # Check if output directory is selected
        if not self.selected_directory:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        # Check if both files are selected
        if not self.file1_path.get() or not self.file2_path.get():
            messagebox.showerror("Error", "Please select both File 1 and File 2.")
            return

        # Add selected files to load order
        self.load_order = [self.file1_path.get(), self.file2_path.get()]

        # Perform the binding using makeself command
        command = self.create_makeself_command()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            messagebox.showinfo("Success", "Files joined successfully.")
        else:
            messagebox.showerror("Error", f"Error joining files:\n{stderr.decode()}")

    def create_makeself_command(self):
        output_file = os.path.join(self.selected_directory, "joined_files.run")

        # Generate the makeself command
        command = [
            "makeself.sh", "--gzip", "--nocomp", "--notemp", "--nocrc",
            self.selected_directory, output_file, "Join Files", *self.load_order
        ]

        return command

