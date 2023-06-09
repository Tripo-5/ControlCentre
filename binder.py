import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class BinderFrame(tk.Frame):
    def __init__(self, root, callback):
        super().__init__(root, width=600, height=400)
        self.callback = callback
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="This is the Binder Frame")
        label.pack()

        back_button = ttk.Button(self, text="Back", command=self.back_button_click)
        back_button.pack()

        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack()

        icon_button = ttk.Button(self, text="Change Icon", command=self.change_icon)
        icon_button.pack()

        load_order_button = ttk.Button(self, text="Change Load Order", command=self.change_load_order)
        load_order_button.pack()

    def back_button_click(self):
        self.callback()

    def join_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Files to Join", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        # TODO: Join the selected files together into a single executable

    def change_icon(self):
        icon_path = filedialog.askopenfilename(title="Select Icon", filetypes=(("Icon Files", "*.ico"), ("All Files", "*.*")))
        # TODO: Change the icon of the executable to the selected icon

    def change_load_order(self):
        # TODO: Implement changing the load order of the executable
