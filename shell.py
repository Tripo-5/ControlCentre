import tkinter as tk
from tkinter import ttk


class ShellFrame(tk.Frame):
    def __init__(self, root, callback):
        super().__init__(root, width=600, height=400)
        self.callback = callback
        self.pack_propagate(0)
        self.create_widgets()
    def create_widgets(self):
        # TODO: Implement the Libraries functionality
        label = ttk.Label(self, text="This is the Shell Frame")
        label.pack()

        self.command_feed_frame = CommandFeedFrame(self)
        self.command_feed_frame.pack(side="left", fill="both", expand=True)

        self.interactive_shell_frame = InteractiveShellFrame(self)
        self.interactive_shell_frame.pack(side="left", fill="both", expand=True)
        
        back_button = ttk.Button(self, text="Back", command=self.back_button_click)
        back_button.pack()

    def back_button_click(self):
        self.callback()    
        
class CommandFeedFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # Create the feed text widget
        self.feed_text = tk.Text(self, wrap="word")
        self.feed_text.pack(side="top", fill="both", expand=True)

        # TODO: Implement functionality to update the feed with running commands


class InteractiveShellFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.pack_propagate(0)
        self.create_widgets()

    def create_widgets(self):
        # Create the shell text widget
        self.shell_text = tk.Text(self, wrap="word")
        self.shell_text.pack(side="top", fill="both", expand=True)

        # TODO: Implement the interactive shell functionality and menu of features
