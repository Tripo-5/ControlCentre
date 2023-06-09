import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class BinderFrame(tk.Frame):
    def __init__(self, root, callback):
        super().__init__(root, width=600, height=400)
        self.callback = callback
        self.pack_propagate(0)
        self.create_widgets()
        self.selected_files = {}  # Dictionary to store selected files for each button
        self.selected_icon = None  # Variable to store selected icon file path
        self.selected_directory = None  # Variable to store selected output directory

    def create_widgets(self):
        label = ttk.Label(self, text="This is the Binder Frame")
        label.pack()

        back_button = ttk.Button(self, text="Back", command=self.back_button_click)
        back_button.pack()

        join_file_button_1 = ttk.Button(self, text="Select File 1", command=lambda: self.select_file(1))
        join_file_button_1.pack()

        file_label_1 = ttk.Label(self, text="")
        file_label_1.pack()
        self.file_labels = [file_label_1]  # List to store file labels for each button

        join_file_button_2 = ttk.Button(self, text="Select File 2", command=lambda: self.select_file(2))
        join_file_button_2.pack()

        file_label_2 = ttk.Label(self, text="")
        file_label_2.pack()
        self.file_labels.append(file_label_2)

        icon_button = ttk.Button(self, text="Change Icon", command=self.change_icon)
        icon_button.pack()

        icon_label = ttk.Label(self, text="")
        icon_label.pack()
        self.icon_label = icon_label

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

        directory_button = ttk.Button(self, text="Change Output Directory", command=self.change_directory)
        directory_button.pack()

        directory_label = ttk.Label(self, text="")
        directory_label.pack()
        self.directory_label = directory_label

        finish_button = ttk.Button(self, text="Finish Binding", command=self.finish_binding)
        finish_button.pack()

    def back_button_click(self):
        self.callback()

    def select_file(self, button_index):
        file_path = filedialog.askopenfilename(title=f"Select File {button_index}", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if file_path:
            self.selected_files[button_index] = file_path
            self.file_labels[button_index - 1]["text"] = file_path

            # Update load order tree with selected files
            self.update_load_order_tree()

    def update_load_order_tree(self):
        self.load_order_tree.delete(*self.load_order_tree.get_children())

        for button_index, file_path in self.selected_files.items():
            self.load_order_tree.insert("", "end", text=f"File {button_index}", values=(file_path,))

    def change_icon(self):
        icon_path = filedialog.askopenfilename(title="Select Icon", filetypes=(("Icon Files", "*.ico"), ("All Files", "*.*")))
        if icon_path:
            self.selected_icon = icon_path
            self.icon_label["text"] = icon_path

    def move_up(self):
        selected_item = self.load_order_tree.selection()
        if selected_item:
            self.load_order_tree.move(selected_item, self.load_order_tree.parent(selected_item), self.load_order_tree.index(selected_item) - 1)

    def move_down(self):
        selected_item = self.load_order_tree.selection()
        if selected_item:
            self.load_order_tree.move(selected_item, self.load_order_tree.parent(selected_item), self.load_order_tree.index(selected_item) + 1)

    def change_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.selected_directory = directory
            self.directory_label["text"] = directory

    def finish_binding(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected.")
            return

        if not self.selected_icon:
            messagebox.showerror("Error", "No icon selected.")
            return

        if not self.selected_directory:
            messagebox.showerror("Error", "No output directory selected.")
            return

        save_path = filedialog.asksaveasfilename(
            title="Save As", defaultextension=".exe",
            filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if not save_path:
            return

    # Join files into a single executable using the selected icon and load order
        output_file = os.path.join(self.selected_directory, os.path.basename(save_path))
        command = [
            "pyinstaller",
            "--onefile",
            "--add-data", f"{self.selected_icon};.",
            "--icon", os.path.basename(self.selected_icon),
            "--distpath", self.selected_directory,
            "--specpath", self.selected_directory
        ]

        for _, file_path in sorted(self.selected_files.items()):
            command.extend(["--add-data", f"{file_path};."])

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            messagebox.showerror("Error", f"Binding process failed:\n{stderr.decode('utf-8')}")
        else:
            messagebox.showinfo("Success", f"Binding process completed.\nOutput file: {output_file}")

    # Clear the selections and reset the labels
        self.selected_files = {}
        self.selected_icon = None
        self.selected_directory = None

        for label in self.file_labels:
            label["text"] = ""

        self.icon_label["text"] = ""
        self.load_order_tree.delete(*self.load_order_tree.get_children())
        self.directory_label["text"] = ""
