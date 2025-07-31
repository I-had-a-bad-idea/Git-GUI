import tkinter as tk
from GUI.startup_window import StartupWindow
from GUI.theme import *
import os.path as path


if __name__ == "__main__":
    root = tk.Tk()
    
    # Set application icon  #FIXME this for some f***ing reason doesn't work when run from .exe
    # path_to_logo = path.abspath(".")
    # path_to_logo = path.join(path_to_logo, "Assets/GUI-Git-Logo.png")
    # icon = tk.PhotoImage(file = path_to_logo)
    # root.iconphoto(True, icon)
    
    # Apply default theme
    root.configure(bg = BG_DARK)
    
    startup_window = StartupWindow(root)
    root.mainloop()
