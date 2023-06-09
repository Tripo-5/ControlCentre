import tkinter as tk
from tkinter import ttk, filedialog
import subprocess

class BinderFrame(ttk.Frame):
    def __init__(self, parent, back_button_click):
        super().__init__(parent)
        self.parent = parent
        self.back_button_click = back_button_click

        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.load_order = []

        self.create_title()
        self.create_file_selection()
        self.create_load_order()
        self.create_output_options()
        self.create_additional_options()
        self.create_join_button()

    def create_title(self):
        title_label = ttk.Label(self, text="File Binder", font=("Helvetica", 18, "bold"))
        title_label.pack(side=tk.TOP, pady=10)

    def create_file_selection(self):
        file_selection_frame = ttk.Frame(self)
        file_selection_frame.pack(side=tk.TOP, pady=10)

        # File 1 selection
        file1_frame = ttk.Frame(file_selection_frame)
        file1_frame.pack(side=tk.TOP, pady=5)
        file1_label = ttk.Label(file1_frame, text="Select File 1")
        file1_label.pack(side=tk.LEFT)
        file1_entry = ttk.Entry(file1_frame, textvariable=self.file1_path, width=50, state="readonly")
        file1_entry.pack(side=tk.LEFT)
        select_file1_button = ttk.Button(file1_frame, text="Browse", command=self.select_file1)
        select_file1_button.pack(side=tk.LEFT)

        # File 2 selection
        file2_frame = ttk.Frame(file_selection_frame)
        file2_frame.pack(side=tk.TOP, pady=5)
        file2_label = ttk.Label(file2_frame, text="Select File 2")
        file2_label.pack(side=tk.LEFT)
        file2_entry = ttk.Entry(file2_frame, textvariable=self.file2_path, width=50, state="readonly")
        file2_entry.pack(side=tk.LEFT)
        select_file2_button = ttk.Button(file2_frame, text="Browse", command=self.select_file2)
        select_file2_button.pack(side=tk.LEFT)

    def create_load_order(self):
        load_order_frame = ttk.Frame(self)
        load_order_frame.pack(side=tk.TOP, pady=10)

        # Load Order label
        load_order_label = ttk.Label(load_order_frame, text="Load Order")
        load_order_label.pack(side=tk.TOP)

        # Load Order Listbox
        load_order_scrollbar = ttk.Scrollbar(load_order_frame)
        self.load_order_listbox = tk.Listbox(load_order_frame, selectmode=tk.SINGLE, yscrollcommand=load_order_scrollbar.set)
        load_order_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.load_order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        load_order_scrollbar.config(command=self.load_order_listbox.yview)

        # Load Order buttons
        buttons_frame = ttk.Frame(load_order_frame)
        buttons_frame.pack(side=tk.TOP, pady=5)
        move_up_button = ttk.Button(buttons_frame, text="Move Up", command=self.move_up)
        move_up_button.pack(side=tk.LEFT)
        move_down_button = ttk.Button(buttons_frame, text="Move Down", command=self.move_down)
        move_down_button.pack(side=tk.LEFT)

    def create_output_options(self):
        output_options_frame = ttk.Frame(self)
        output_options_frame.pack(side=tk.TOP, pady=10)

        # Output Directory selection
        output_directory_frame = ttk.Frame(output_options_frame)
        output_directory_frame.pack(side=tk.TOP, pady=5)
        output_directory_label = ttk.Label(output_directory_frame, text="Output Directory")
        output_directory_label.pack(side=tk.LEFT)
        output_directory_entry = ttk.Entry(output_directory_frame, textvariable=self.output_directory, width=50, state="readonly")
        output_directory_entry.pack(side=tk.LEFT)
        select_output_directory_button = ttk.Button(output_directory_frame, text="Browse", command=self.select_output_directory)
        select_output_directory_button.pack(side=tk.LEFT)

        # Output Filename selection
        output_filename_frame = ttk.Frame(output_options_frame)
        output_filename_frame.pack(side=tk.TOP, pady=5)
        output_filename_label = ttk.Label(output_filename_frame, text="Output Filename")
        output_filename_label.pack(side=tk.LEFT)
        output_filename_entry = ttk.Entry(output_filename_frame, textvariable=self.output_filename, width=50)
        output_filename_entry.pack(side=tk.LEFT)

    def create_additional_options(self):
        additional_options_frame = ttk.Frame(self)
        additional_options_frame.pack(side=tk.TOP, pady=10)

        # Icon selection
        icon_frame = ttk.Frame(additional_options_frame)
        icon_frame.pack(side=tk.TOP, pady=5)
        icon_label = ttk.Label(icon_frame, text="Select Icon")
        icon_label.pack(side=tk.LEFT)
        select_icon_button = ttk.Button(icon_frame, text="Browse", command=self.select_icon)
        select_icon_button.pack(side=tk.LEFT)

        # OS selection
        os_frame = ttk.Frame(additional_options_frame)
        os_frame.pack(side=tk.TOP, pady=5)
        os_label = ttk.Label(os_frame, text="Operating System")
        os_label.pack(side=tk.LEFT)
        self.os_combobox = ttk.Combobox(os_frame, values=["Windows", "Linux"])
        self.os_combobox.pack(side=tk.LEFT)

        # Post Installation Scripts selection
        post_installation_frame = ttk.Frame(additional_options_frame)
        post_installation_frame.pack(side=tk.TOP, pady=5)
        post_installation_label = ttk.Label(post_installation_frame, text="Post Installation Scripts")
        post_installation_label.pack(side=tk.LEFT)
        self.post_installation_var = tk.StringVar()
        self.post_installation_checkboxes = []
        post_installation_scripts = [
            "Script 1",
            "Script 2",
            "Script 3",
            # Add more script options as needed
        ]
        for script in post_installation_scripts:
            checkbox = ttk.Checkbutton(post_installation_frame, text=script, variable=self.post_installation_var)
            checkbox.pack(side=tk.LEFT)
            self.post_installation_checkboxes.append(checkbox)

    def create_join_button(self):
        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack(side=tk.TOP, pady=20)

    def select_file1(self):
      file_path = filedialog.askopenfilename(title="Select File 1", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
      if file_path:
          self.selected_files[1] = file_path
          self.file_labels[0]["text"] = file_path

          # Update load order tree with selected files
           self.update_load_order_tree()

    def select_file2(self):
        file_path = filedialog.askopenfilename(title="Select File 2", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if file_path:
            self.selected_files[2] = file_path
           self.file_labels[1]["text"] = file_path

           # Update load order tree with selected files
          self.update_load_order_tree()

    def select_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory.set(directory)

    def select_icon(self):
        icon_path = filedialog.askopenfilename()
        # TODO: Handle selected icon path

    def move_up(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index > 0:
                item = self.load_order_listbox.get(selected_index)
                self.load_order_listbox.delete(selected_index)
                self.load_order_listbox.insert(selected_index - 1, item)
                self.load_order_listbox.selection_set(selected_index - 1)

    def move_down(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            if selected_index < self.load_order_listbox.size() - 1:
                item = self.load_order_listbox.get(selected_index)
                self.load_order_listbox.delete(selected_index)
                self.load_order_listbox.insert(selected_index + 1, item)
                self.load_order_listbox.selection_set(selected_index + 1)

    def join_files(self):
        file1 = self.file1_path.get()
        file2 = self.file2_path.get()
        output_directory = self.output_directory.get()
        output_filename = self.output_filename.get()
        selected_files = self.load_order_listbox.get(0, tk.END)
        icon_path = ""  # TODO: Get selected icon path
        selected_os = self.os_combobox.get()
        selected_scripts = [checkbox.cget("text") for checkbox in self.post_installation_checkboxes if checkbox.instate(["selected"])]

        # TODO: Implement file joining logic
        print("File 1:", file1)
        print("File 2:", file2)
        print("Output Directory:", output_directory)
        print("Output Filename:", output_filename)
        print("Selected Files:", selected_files)
        print("Icon Path:", icon_path)
        print("Selected OS:", selected_os)
        print("Selected Scripts:", selected_scripts)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Binder")
        self.geometry("600x600")

        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.current_frame = None
        self.show_binder_frame()

    def show_binder_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = BinderFrame(self.container, self.show_main_frame)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_main_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainFrame(self.container, self.show_binder_frame)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

class MainFrame(ttk.Frame):
    def __init__(self, parent, next_button_click):
        super().__init__(parent)
        self.parent = parent
        self.next_button_click = next_button_click

        self.create_title()
        self.create_next_button()

    def create_title(self):
        title_label = ttk.Label(self, text="Main Menu", font=("Helvetica", 18, "bold"))
        title_label.pack(side=tk.TOP, pady=10)

    def create_next_button(self):
        next_button = ttk.Button(self, text="Next", command=self.next_button_click)
        next_button.pack(side=tk.TOP, pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
