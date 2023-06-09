import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

class BinderFrame(ttk.Frame):
    def __init__(self, parent, back_button_click):
        super().__init__(parent)
        self.parent = parent
        self.back_button_click = back_button_click
        self.selected_files = []
        self.load_order = []

        self.create_title()
        self.create_file_selection()
        self.create_load_order()
        self.create_output_options()
        self.create_additional_options()
        self.create_join_button()

    def create_title(self):
        title_label = ttk.Label(self, text="Binder Options", font=("Helvetica", 24))
        title_label.pack(side=tk.TOP, pady=20)

    def create_file_selection(self):
        file_selection_frame = ttk.Frame(self)
        file_selection_frame.pack(side=tk.LEFT, padx=10)

        # Create File Selection label
        file_selection_label = ttk.Label(file_selection_frame, text="File Selection")
        file_selection_label.pack(side=tk.TOP)

        # Create Select File 1 button and display box
        file1_selection_frame = ttk.Frame(file_selection_frame)
        file1_selection_frame.pack(side=tk.TOP, pady=5)
        select_file1_button = ttk.Button(file1_selection_frame, text="Select File 1", command=self.select_file1)
        select_file1_button.pack(side=tk.LEFT)
        self.file1_path = tk.StringVar()
        file1_display = ttk.Entry(file1_selection_frame, textvariable=self.file1_path, width=30, state="readonly")
        file1_display.pack(side=tk.LEFT)

        # Create Select File 2 button and display box
        file2_selection_frame = ttk.Frame(file_selection_frame)
        file2_selection_frame.pack(side=tk.TOP, pady=5)
        select_file2_button = ttk.Button(file2_selection_frame, text="Select File 2", command=self.select_file2)
        select_file2_button.pack(side=tk.LEFT)
        self.file2_path = tk.StringVar()
        file2_display = ttk.Entry(file2_selection_frame, textvariable=self.file2_path, width=30, state="readonly")
        file2_display.pack(side=tk.LEFT)

    def create_load_order(self):
        load_order_frame = ttk.Frame(self)
        load_order_frame.pack(side=tk.LEFT, padx=10)

        # Create Load Order label
        load_order_label = ttk.Label(load_order_frame, text="Load Order")
        load_order_label.pack(side=tk.TOP)

        # Create Load Order Listbox
        self.load_order_listbox = tk.Listbox(load_order_frame, selectmode=tk.SINGLE, width=30, height=5)
        self.load_order_listbox.pack(side=tk.TOP, pady=5)

        # Create Move Up and Move Down buttons
        move_up_button = ttk.Button(load_order_frame, text="Move Up", command=self.move_up)
        move_up_button.pack(side=tk.LEFT)
        move_down_button = ttk.Button(load_order_frame, text="Move Down", command=self.move_down)
        move_down_button.pack(side=tk.LEFT)

    def create_output_options(self):
        output_options_frame = ttk.Frame(self)
        output_options_frame.pack(side=tk.LEFT, padx=10)

        # Create Output Options label
        output_options_label = ttk.Label(output_options_frame, text="Output Options")
        output_options_label.pack(side=tk.TOP)

        # Create Output Filename selection
        output_filename_frame = ttk.Frame(output_options_frame)
        output_filename_frame.pack(side=tk.TOP, pady=5)
        output_filename_label = ttk.Label(output_filename_frame, text="Output Filename")
        output_filename_label.pack(side=tk.LEFT)
        self.output_filename_entry = ttk.Entry(output_filename_frame, width=30)
        self.output_filename_entry.pack(side=tk.LEFT)

        # Create Icon selection
        icon_frame = ttk.Frame(output_options_frame)
        icon_frame.pack(side=tk.TOP, pady=5)
        icon_label = ttk.Label(icon_frame, text="Icon")
        icon_label.pack(side=tk.LEFT)
        self.icon_path = tk.StringVar()
        icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_path, width=30, state="readonly")
        icon_entry.pack(side=tk.LEFT)
        select_icon_button = ttk.Button(icon_frame, text="Select Icon", command=self.select_icon)
        select_icon_button.pack(side=tk.LEFT)

    def create_additional_options(self):
        additional_options_frame = ttk.Frame(self)
        additional_options_frame.pack(side=tk.LEFT, padx=10)

        # Create Additional Options label
        additional_options_label = ttk.Label(additional_options_frame, text="Additional Options")
        additional_options_label.pack(side=tk.TOP)

        # TODO: Add checkboxes or input fields for additional options

    def create_join_button(self):
        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack(side=tk.TOP, pady=20)

    def select_file1(self):
        file_path = filedialog.askopenfilename()
        self.file1_path.set(file_path)

    def select_file2(self):
        file_path = filedialog.askopenfilename()
        self.file2_path.set(file_path)

    def move_up(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index > 0:
                item = self.load_order.pop(selected_index)
                self.load_order.insert(selected_index - 1, item)
                self.update_load_order_listbox(selected_index - 1)

    def move_down(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < len(self.load_order) - 1:
                item = self.load_order.pop(selected_index)
                self.load_order.insert(selected_index + 1, item)
                self.update_load_order_listbox(selected_index + 1)

    def update_load_order_listbox(self, selected_index):
        self.load_order_listbox.delete(0, tk.END)
        for item in self.load_order:
            self.load_order_listbox.insert(tk.END, item)
        self.load_order_listbox.select_set(selected_index)

    def select_icon(self):
        icon_path = filedialog.askopenfilename()
        self.icon_path.set(icon_path)

    def join_files(self):
        # Retrieve the selected files
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        self.selected_files = [file1, file2]

        # Retrieve the load order
        self.load_order = list(self.load_order_listbox.get(0, tk.END))

        # Retrieve the output options
        output_filename = self.output_filename_entry.get()
        icon_path = self.icon_path.get()

        # TODO: Retrieve values from checkboxes or input fields for additional options

        # Print the selected files, output filename, icon, load order, and additional options
        print("Selected Files:")
        for file in self.selected_files:
            print(file)
        print("Output Filename:", output_filename)
        print("Icon:", icon_path)
        print("Load Order:")
        for item in self.load_order:
            print(item)
        print("Additional Options:")
        # TODO: Print additional options

    def back_button_click(self):
        self.destroy()
        self.back_button_click()
