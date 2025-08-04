import tkinter as tk
from GUI.startup_window import StartupWindow
from GUI.theme import *
import os
import sys



def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS #type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    root = tk.Tk()
            
    icon = tk.PhotoImage(file = resource_path("GUI-Git-Logo.png"))
    root.iconphoto(True, icon)
    # Apply default theme
    root.configure(bg = BG_DARK) #dark mode, yeah
    
    startup_window = StartupWindow(root)
    root.mainloop()