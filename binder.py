import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class BinderFrame(ttk.Frame):
    def __init__(self, parent, back_button_click):
        super().__init__(parent)
        self.parent = parent
        self.back_button_click = back_button_click

        self.selected_files = []
        self.selected_directory = ""
        self.load_order = []

        self.create_file_selection()
        self.create_load_order()
        self.create_directory_selection()
        self.create_binder_selection()
        self.create_post_install_script()
        self.create_additional_options()
        self.create_join_button()

    def create_file_selection(self):
        file_selection_frame = ttk.Frame(self)
        file_selection_frame.pack(side=tk.LEFT, padx=10)

        # Create Select File 1 button
        select_file1_button = ttk.Button(file_selection_frame, text="Select File 1", command=self.select_file1)
        select_file1_button.pack(side=tk.TOP, pady=5)

        # Create File 1 display box
        self.file1_path = tk.StringVar()
        file1_display_box = ttk.Entry(file_selection_frame, textvariable=self.file1_path, state="readonly")
        file1_display_box.pack(side=tk.TOP, pady=5)

        # Create Select File 2 button
        select_file2_button = ttk.Button(file_selection_frame, text="Select File 2", command=self.select_file2)
        select_file2_button.pack(side=tk.TOP, pady=5)

        # Create File 2 display box
        self.file2_path = tk.StringVar()
        file2_display_box = ttk.Entry(file_selection_frame, textvariable=self.file2_path, state="readonly")
        file2_display_box.pack(side=tk.TOP, pady=5)

    def create_load_order(self):
        load_order_frame = ttk.Frame(self)
        load_order_frame.pack(side=tk.LEFT, padx=10)

        # Create Load Order label
        load_order_label = ttk.Label(load_order_frame, text="Load Order")
        load_order_label.pack(side=tk.TOP)

        # Create Load Order Listbox
        self.load_order_listbox = tk.Listbox(load_order_frame, height=5, selectmode=tk.SINGLE)
        self.load_order_listbox.pack(side=tk.TOP, pady=5)

        # Create Move Up button
        move_up_button = ttk.Button(load_order_frame, text="Move Up", command=self.move_up)
        move_up_button.pack(side=tk.TOP)

        # Create Move Down button
        move_down_button = ttk.Button(load_order_frame, text="Move Down", command=self.move_down)
        move_down_button.pack(side=tk.TOP)

    def create_directory_selection(self):
        directory_selection_frame = ttk.Frame(self)
        directory_selection_frame.pack(side=tk.LEFT, padx=10)

        # Create Select Directory button
        select_directory_button = ttk.Button(directory_selection_frame, text="Select Directory", command=self.select_directory)
        select_directory_button.pack(side=tk.TOP, pady=5)

        # Create Directory display box
        self.directory_path = tk.StringVar()
        directory_display_box = ttk.Entry(directory_selection_frame, textvariable=self.directory_path, state="readonly")
        directory_display_box.pack(side=tk.TOP, pady=5)

    def create_binder_selection(self):
        binder_selection_frame = ttk.Frame(self)
        binder_selection_frame.pack(side=tk.LEFT, padx=10)

        # Create Binder Selection label
        binder_selection_label = ttk.Label(binder_selection_frame, text="Binder Selection")
        binder_selection_label.pack(side=tk.TOP)

        # Create Binder Selection buttons
        binders = ["IExpress", "Makeself"]
        self.binder_var = tk.StringVar()
        for binder in binders:
            btn = ttk.Radiobutton(binder_selection_frame, text=binder, variable=self.binder_var, value=binder)
            btn.pack(side=tk.TOP, pady=5)

    def create_post_install_script(self):
        post_install_script_frame = ttk.Frame(self)
        post_install_script_frame.pack(side=tk.LEFT, padx=10)

        # Create Post-Install Script label
        post_install_script_label = ttk.Label(post_install_script_frame, text="Post-Install Script")
        post_install_script_label.pack(side=tk.TOP)

        # Create Post-Install Script text box
        self.post_install_script_text = tk.Text(post_install_script_frame, height=5, width=30)
        self.post_install_script_text.pack(side=tk.TOP, pady=5)

    def create_additional_options(self):
        additional_options_frame = ttk.Frame(self)
        additional_options_frame.pack(side=tk.LEFT, padx=10)

        # Create Additional Options label
        additional_options_label = ttk.Label(additional_options_frame, text="Additional Options")
        additional_options_label.pack(side=tk.TOP)

        # TODO: Add code to create checkboxes or other input fields for additional options

    def create_join_button(self):
        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack(side=tk.BOTTOM, pady=10)

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
                self.load_order_listbox.delete(selected_index)
                self.load_order_listbox.insert(selected_index - 1, self.load_order[selected_index])
                self.load_order.pop(selected_index)
                self.load_order.insert(selected_index - 1, self.selected_files[selected_index])
                self.load_order_listbox.selection_clear(0, tk.END)
                self.load_order_listbox.selection_set(selected_index - 1)

    def move_down(self):
        selected_index = self.load_order_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < len(self.load_order) - 1:
                self.load_order_listbox.delete(selected_index)
                self.load_order_listbox.insert(selected_index + 1, self.load_order[selected_index])
                self.load_order.pop(selected_index)
                self.load_order.insert(selected_index + 1, self.selected_files[selected_index])
                self.load_order_listbox.selection_clear(0, tk.END)
                self.load_order_listbox.selection_set(selected_index + 1)

    def select_directory(self):
        directory_path = filedialog.askdirectory()
        self.directory_path.set(directory_path)

    def join_files(self):
        # Check if the directory is selected
        if not self.directory_path.get():
            messagebox.showerror("Error", "Please select the output directory.")
            return

        # Check if at least two files are selected
        if len(self.selected_files) < 2:
            messagebox.showerror("Error", "Please select at least two files.")
            return

        # Check if binder is selected
        self.selected_binder = self.binder_var.get()
        if not self.selected_binder:
            messagebox.showerror("Error", "Please select a binder.")
            return

        # Get the post-install script content
        post_install_script = self.post_install_script_text.get("1.0", tk.END).strip()

        # Get the additional options
        # TODO: Retrieve values from checkboxes or input fields for additional options

        # Print the selected files, output directory, binder, post-install script, and additional options
        print("Selected Files:")
        for file in self.selected_files:
            print(file)
        print("Output Directory:", self.directory_path.get())
        print("Binder:", self.selected_binder)
        print("Post-Install Script:")
        print(post_install_script)
        print("Additional Options:")
        # TODO: Print the values of additional options

    def back_button_click(self):
        self.destroy()
        self.parent.show_main_frame()

class MainFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.create_title()
        self.create_buttons()

    def create_title(self):
        title_label = ttk.Label(self, text="Binder Application", font=("Helvetica", 24))
        title_label.pack(side=tk.TOP, pady=20)

    def create_buttons(self):
        button_options = [
            ("Select Files", self.select_files_click),
            ("Binder Options", self.binder_options_click),
            ("Join Files", self.join_files_click),
            ("Exit", self.exit_click)
        ]

        for option in button_options:
            btn = ttk.Button(self, text=option[0], command=option[1])
            btn.pack(side=tk.TOP, pady=10)

    def select_files_click(self):
        self.hide_main_frame()
        binder_frame = BinderFrame(self, self.show_main_frame)

    def binder_options_click(self):
        messagebox.showinfo("Binder Options", "Not implemented yet!")

    def join_files_click(self):
        messagebox.showinfo("Join Files", "Not implemented yet!")

    def exit_click(self):
        self.parent.destroy()

    def show_main_frame(self):
        self.pack()

    def hide_main_frame(self):
        self.pack_forget()
