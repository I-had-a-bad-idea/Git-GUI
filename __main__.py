import tkinter as tk
from GUI.startup_window import StartupWindow
from GUI.theme import *


if __name__ == "__main__":
    root = tk.Tk()
    
    # Apply default theme
    root.configure(bg = BG_DARK)
    
    startup_window = StartupWindow(root)
    root.mainloop()