import tkinter as tk
from tkinter import ttk


class ConnectionsFrame(tk.Frame):
    def __init__(self, root, callback):
        super().__init__(root, width=600, height=400)
        self.callback = callback
        self.pack_propagate(0)
        self.create_widgets()
    def create_widgets(self):
        # TODO: Implement the binder functionality
        label = ttk.Label(self, text="This is the Connections Frame")
        label.pack()

        back_button = ttk.Button(self, text="Back", command=self.back_button_click)
        back_button.pack()

    def back_button_click(self):
        self.callback()    
