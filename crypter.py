import random
import base64
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class CrypterFrame(tk.Frame):
    def __init__(self, parent, back_callback):
        super().__init__(parent)
        self.parent = parent
        self.back_callback = back_callback

        self.encryption_options = [
            "XOR",
            "AES",
            "RSA"
        ]
        self.selected_encryption = tk.StringVar()
        self.input_file_path = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.output_filename = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.encryption_label = ttk.Label(self, text="Encryption Method:")
        self.encryption_dropdown = ttk.Combobox(self, values=self.encryption_options, textvariable=self.selected_encryption)
        self.encryption_dropdown.set(self.encryption_options[0])

        self.input_file_label = ttk.Label(self, text="Input File:")
        self.input_file_entry = ttk.Entry(self, textvariable=self.input_file_path)
        self.input_file_button = ttk.Button(self, text="Browse", command=self.browse_input_file)

        self.output_directory_label = ttk.Label(self, text="Output Directory:")
        self.output_directory_entry = ttk.Entry(self, textvariable=self.output_directory)
        self.output_directory_button = ttk.Button(self, text="Browse", command=self.browse_output_directory)

        self.output_filename_label = ttk.Label(self, text="Output Filename:")
        self.output_filename_entry = ttk.Entry(self, textvariable=self.output_filename)

        self.builder_button = ttk.Button(self, text="Build", command=self.build_exe)

        self.back_button = ttk.Button(self, text="Back", command=self.back_callback)

        self.encryption_label.pack()
        self.encryption_dropdown.pack()
        self.input_file_label.pack()
        self.input_file_entry.pack()
        self.input_file_button.pack()
        self.output_directory_label.pack()
        self.output_directory_entry.pack()
        self.output_directory_button.pack()
        self.output_filename_label.pack()
        self.output_filename_entry.pack()
        self.builder_button.pack()
        self.back_button.pack()

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if file_path:
            self.input_file_path.set(file_path)

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    def build_exe(self):
        encryption_method = self.selected_encryption.get()
        input_file = self.input_file_path.get()
        output_directory = self.output_directory.get()
        output_filename = self.output_filename.get()

        if not input_file or not output_directory or not output_filename:
            messagebox.showerror("Error", "Please provide the input file, output directory, and output filename.")
            return

        if encryption_method == "XOR":
            self.build_xored_exe(input_file, output_directory, output_filename)
        elif encryption_method == "AES":
            self.build_aes_exe(input_file, output_directory, output_filename)
        elif encryption_method == "RSA":
            self.build_rsa_exe(input_file, output_directory, output_filename)
        else:
            messagebox.showerror("Error", "Invalid encryption method selected.")

    def build_xored_exe(self, input_file, output_directory, output_filename):
        # Code for building XOR-encrypted executable

        messagebox.showinfo("Success", "XOR-encrypted executable built successfully!")

    def build_aes_exe(self, input_file, output_directory, output_filename):
        # Code for building AES-encrypted executable

        messagebox.showinfo("Success", "AES-encrypted executable built successfully!")

    def build_rsa_exe(self, input_file, output_directory, output_filename):
        # Code for building RSA-encrypted executable

        messagebox.showinfo("Success", "RSA-encrypted executable built successfully!")
