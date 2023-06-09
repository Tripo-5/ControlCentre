import tkinter as tk
import PyInstaller.__main__ as pyinstaller
import random
import base64
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class BuilderFrame(tk.Frame):
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

        if not input_file or not output_directory:
            messagebox.showerror("Error", "Please select an input file and output directory.")
            return

        if encryption_method == "XOR":
            self.build_xored_exe(input_file, output_directory)
        elif encryption_method == "AES":
            self.build_aes_exe(input_file, output_directory)
        elif encryption_method == "RSA":
            self.build_rsa_exe(input_file, output_directory)
        else:
            messagebox.showerror("Error", "Invalid encryption method selected.")

    def build_xored_exe(self, input_file, output_directory):
        # Your existing code for generating the builder

        messagebox.showinfo("Success", "XOR-encrypted builder code generated successfully!")

    def build_aes_exe(self, input_file, output_directory):
        # Your code for generating the builder with AES encryption

        messagebox.showinfo("Success", "AES-encrypted builder code generated successfully!")

    def build_rsa_exe(self, input_file, output_directory):
        # Your code for generating the builder with RSA encryption

        messagebox.showinfo("Success", "RSA-encrypted builder code generated successfully!")
