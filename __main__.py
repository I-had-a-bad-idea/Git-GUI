import tkinter as tk
from GUI.startup_window import StartupWindow


if __name__ == "__main__":
    root = tk.Tk()
    startup_window = StartupWindow(root)
    root.mainloop()