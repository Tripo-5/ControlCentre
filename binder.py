import os
import subprocess
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
        self.selected_files = []  # List to store selected files
        self.selected_output_directory = None  # Variable to store selected output directory

    def create_widgets(self):
        label = ttk.Label(self, text="This is the Binder Frame")
        label.pack()

        back_button = ttk.Button(self, text="Back", command=self.back_button_click)
        back_button.pack()

        select_file_button = ttk.Button(self, text="Select File", command=self.select_file)
        select_file_button.pack()

        file_label = ttk.Label(self, text="")
        file_label.pack()
        self.file_label = file_label

        directory_button = ttk.Button(self, text="Change Output Directory", command=self.change_directory)
        directory_button.pack()

        directory_label = ttk.Label(self, text="")
        directory_label.pack()
        self.directory_label = directory_label

        # Checkbox and textbox for selecting the tool (IExpress or makeself)
        tool_frame = ttk.Frame(self)
        tool_frame.pack(pady=10)

        tool_label = ttk.Label(tool_frame, text="Select Tool:")
        tool_label.grid(row=0, column=0, sticky="w")

        self.selected_tool = tk.StringVar()
        self.selected_tool.set("IExpress")  # Default selection

        tool_radiobutton_iexpress = ttk.Radiobutton(tool_frame, text="IExpress", variable=self.selected_tool, value="IExpress")
        tool_radiobutton_iexpress.grid(row=0, column=1, sticky="w")

        tool_radiobutton_makeself = ttk.Radiobutton(tool_frame, text="makeself", variable=self.selected_tool, value="makeself")
        tool_radiobutton_makeself.grid(row=0, column=2, sticky="w")

        # Checkbox for compression option
        self.compress_var = tk.BooleanVar()
        self.compress_var.set(True)  # Default selection

        compress_checkbox = ttk.Checkbutton(self, text="Compress Files", variable=self.compress_var)
        compress_checkbox.pack()

        # Textbox for post-extraction command
        post_command_label = ttk.Label(self, text="Post-Extraction Command:")
        post_command_label.pack()

        self.post_command_entry = ttk.Entry(self, width=50)
        self.post_command_entry.pack()

        join_button = ttk.Button(self, text="Join Files", command=self.join_files)
        join_button.pack()

    def back_button_click(self):
        self.callback()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select File", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if file_path:
            self.selected_files.append(file_path)
            self.file_label["text"] = file_path

    def change_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.selected_output_directory = directory
            self.directory_label["text"] = directory

    def join_files(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected.")
            return

        if not self.selected_output_directory:
            messagebox.showerror("Error", "No output directory selected.")
            return

        output_file = filedialog.asksaveasfilename(title="Save Joined File", filetypes=(("Executable Files", "*.exe"), ("All Files", "*.*")))
        if not output_file:
            return

        if self.selected_tool.get() == "IExpress":
            self.join_files_with_iexpress(output_file)
        elif self.selected_tool.get() == "makeself":
            self.join_files_with_makeself(output_file)

    def join_files_with_iexpress(self, output_file):
        # Create the temporary batch file to run the joined files
        temp_batch_file = os.path.join(self.selected_output_directory, "temp_batch.bat")
        with open(temp_batch_file, "w") as file:
            file.write("@echo off\n")
            for file_path in self.selected_files:
                file.write(f'call "{file_path}"\n')
            post_command = self.post_command_entry.get()
            if post_command:
                file.write(f'{post_command}\n')

        # Create the configuration file for IExpress
        config_file = os.path.join(self.selected_output_directory, "config.txt")
        with open(config_file, "w") as file:
            file.write("[Version]\n")
            file.write("Class=IEXPRESS\n")
            file.write("SEDVersion=3\n")
            file.write("[Options]\n")
            file.write("PackagePurpose=InstallApp\n")
            file.write("ShowInstallProgramWindow=0\n")
            if self.compress_var.get():
                file.write("HideExtractAnimation=1\n")
            else:
                file.write("HideExtractAnimation=0\n")
            file.write("UseLongFileName=1\n")
            file.write("InsideCompressed=0\n")
            file.write("[Strings]\n")
            file.write("InstallPrompt=\n")
            file.write("DisplayLicense=\n")
            file.write("FinishMessage=\n")
            file.write("TargetName=temp.exe\n")
            file.write("FriendlyName=Joined Files\n")
            file.write(f"AppLaunched=cmd /c \"{temp_batch_file}\"\n")
            file.write("PostInstallCmd=<None>\n")
            file.write("AdminQuietInstCmd=\n")
            file.write("UserQuietInstCmd=\n")

        # Execute IExpress to create the self-extracting executable
        iexpress_command = ["iexpress", "/n", "/q", "/m", config_file]
        subprocess.run(iexpress_command, cwd=self.selected_output_directory, shell=True)

        # Remove the temporary batch file and the configuration file
        os.remove(temp_batch_file)
        os.remove(config_file)

        messagebox.showinfo("Success", f"Joining process completed.\nOutput file: {output_file}")

    def join_files_with_makeself(self, output_file):
        # Create the command to join the files using makeself
        makeself_command = ["makeself.sh", "--tar-quiet", "--nocomp", "--notemp", "--nox11", "--nomd5"]
        makeself_command.extend(self.selected_files)
        makeself_command.append(output_file)

        # Execute makeself to create the self-extracting executable
        process = subprocess.Popen(makeself_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            messagebox.showerror("Error", f"Joining process failed:\n{stderr.decode('utf-8')}")
        else:
            messagebox.showinfo("Success", f"Joining process completed.\nOutput file: {output_file}")

        # Clear the selections and reset the labels
        self.selected_files = []
        self.selected_output_directory = None
        self.file_label["text"] = ""
        self.directory_label["text"] = ""
