import tkinter as tk
from gui import ControlCommandCenterGUI

root = tk.Tk()
root.title("Control and Command Center")
root.geometry("800x600")

gui = ControlCommandCenterGUI(root)

root.mainloop()
