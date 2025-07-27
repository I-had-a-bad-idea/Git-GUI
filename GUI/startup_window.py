import tkinter as tk
from tkinter import filedialog, messagebox
from git_interface import git_commands
from .gui_window import GUIWindow
from .theme import *
import os

class StartupWindow:
    def __init__(self, root):
        self.root = root
        root.title("Git GUI")
        root.geometry("400x300")
        root.configure(bg = BG_DARK)
        
        # Set window icon for this window as well

        # Center frame for buttons
        main_frame = tk.Frame(root, bg = BG_DARK)
        main_frame.pack(expand = True)

        # Title
        title = tk.Label(main_frame, 
                        text = "Git Repository", 
                        **LABEL_STYLE)
        title.pack(pady = 20)

        # Buttons
        open_button = tk.Button(main_frame, 
                              text = "Open Existing Repository",
                              command = self.open_repository,
                              **BUTTON_STYLE)
        open_button.pack(pady = 10)

        create_button = tk.Button(main_frame,
                                text = "Create New Repository",
                                command = self.create_repository,
                                **BUTTON_STYLE)
        create_button.pack(pady = 10)

        clone_button = tk.Button(main_frame,
                               text = "Clone Repository",
                               command = self.clone_repository,
                               **BUTTON_STYLE)
        clone_button.pack(pady = 10)

    def open_repository(self):
        path = filedialog.askdirectory(title = "Select Git Repository")
        if path:
            # Check if it's a valid git repo by trying to get current branch
            branch = git_commands.get_current_branch(path)
            if branch:
                self.open_main_window(path)
            else:
                messagebox.showerror("Error", "Selected directory is not a Git repository")

    def create_repository(self):
        path = filedialog.askdirectory(title = "Select Directory for New Repository")
        if path:
            success, message = git_commands.init_repo(path)
            if success:
                self.open_main_window(path)
            else:
                messagebox.showerror("Error", f"Could not create repository: {message}")

    def clone_repository(self):
        # Create clone dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Clone Repository")
        dialog.geometry("500x200")
        dialog.config(bg = "gray20")
        dialog.transient(self.root)
        dialog.grab_set()

        # URL entry
        url_frame = tk.Frame(dialog, bg = "gray20")
        url_frame.pack(fill = "x", padx = 20, pady = 10)
        
        url_label = tk.Label(url_frame, text = "URL:", bg = "gray20", fg  = "white")
        url_label.pack(side = "left")
        
        url_entry = tk.Entry(url_frame, width = 50, bg = "gray30", fg = "white")
        url_entry.pack(side = "left", padx = 10)

        # Directory selection
        dir_frame = tk.Frame(dialog, bg = "gray20")
        dir_frame.pack(fill = "x", padx = 20, pady = 10)
        
        dir_label = tk.Label(dir_frame, text = "Directory:", bg = "gray20", fg = "white")
        dir_label.pack(side = "left")
        
        dir_entry = tk.Entry(dir_frame, width = 40, bg = "gray30", fg = "white")
        dir_entry.pack(side = "left", padx = 10)
        
        browse_button = tk.Button(dir_frame, 
                             text = "Browse",
                             command = lambda: dir_entry.insert(0, filedialog.askdirectory()),
                             bg = "gray30", fg = "white")
        browse_button.pack(side = "left")

        # Clone button
        def clone():
            url = url_entry.get()
            path = dir_entry.get()
            if url and path:
                repo_name = url.split("/")[-1].replace(".git", "")
                destination = os.path.join(path, repo_name)
                success, message = git_commands.clone_repo(url, destination)
                if success:
                    dialog.destroy()
                    self.open_main_window(destination)
                else:
                    messagebox.showerror("Error", f"Clone failed: {message}")
            else:
                messagebox.showerror("Error", "Please fill in both URL and directory")

        clone_button = tk.Button(dialog,
                            text = "Clone",
                            command = clone,
                            bg = "gray30", 
                            fg = "white")
        clone_button.pack(pady = 20)

    def open_main_window(self, repo_path):
        # Hide startup window
        self.root.withdraw()
        
        # Create new window for repository
        repo_window = tk.Toplevel()
        gui = GUIWindow(repo_window)
        gui.repo_path = repo_path
        gui.repo_path_var.set(repo_path)
        
        # Try to get remote URL
        url = git_commands.get_remote_url(repo_path)
        if url:
            gui.repo_url = url
            gui.repo_url_var.set(url)

        gui.refresh_lists()

        # When repo window is closed, show startup window again
        def on_closing():
            repo_window.destroy()
            self.root.deiconify()

        repo_window.protocol("WM_DELETE_WINDOW", on_closing)