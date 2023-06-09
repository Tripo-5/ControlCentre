import tkinter as tk
from tkinter import ttk
import PyInstaller.__main__ as pyinstaller


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

        self.create_widgets()

    def create_widgets(self):
        self.encryption_label = ttk.Label(self, text="Encryption Method:")
        self.encryption_dropdown = ttk.Combobox(self, values=self.encryption_options, textvariable=self.selected_encryption)
        self.encryption_dropdown.set(self.encryption_options[0])

        self.builder_button = ttk.Button(self, text="Build", command=self.build_exe)

        self.back_button = ttk.Button(self, text="Back", command=self.back_callback)

        self.encryption_label.pack()
        self.encryption_dropdown.pack()
        self.builder_button.pack()
        self.back_button.pack()

    def build_exe(self):
        encryption_method = self.selected_encryption.get()

        if encryption_method == "XOR":
            self.build_xored_exe()
        elif encryption_method == "AES":
            self.build_aes_exe()
        elif encryption_method == "RSA":
            self.build_rsa_exe()
        else:
            messagebox.showerror("Error", "Invalid encryption method selected.")

    def build_xored_exe(self):
        # Your existing code for generating the builder

        messagebox.showinfo("Success", "XOR-encrypted builder code generated successfully!")

    def build_aes_exe(self):
        # Your code for generating the builder with AES encryption

        messagebox.showinfo("Success", "AES-encrypted builder code generated successfully!")

    def build_rsa_exe(self):
        # Your code for generating the builder with RSA encryption

        messagebox.showinfo("Success", "RSA-encrypted builder code generated successfully!")



