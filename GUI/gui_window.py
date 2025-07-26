import tkinter as tk
from tkinter import filedialog, messagebox
from git_interface import git_commands

# Color 

# Background colors
BG_DARK = "gray20"
BG_DARKER = "gray15"
BG_LIGHTER = "gray25"
BG_BUTTON = "gray30"

# Text colors
TEXT_NORMAL = "white"

# Fonts
FONT_NORMAL = ("Arial", 11)
FONT_SMALL = ("Arial", 10)
FONT_TITLE = ("Arial", 12)
FONT_MONO = ("Arial", 12)

class GUIWindow:
    def __init__(self, root) -> None:
        # Instance-specific repository paths
        self.repo_path = ""
        self.repo_url = ""

        # Common styles
        self.button_style = {
            "width": 12, 
            "font": FONT_NORMAL, 
            "bg": BG_BUTTON, 
            "fg": TEXT_NORMAL
        }

        self.label_style = {
            "bg": BG_DARK,
            "fg": TEXT_NORMAL,
            "font": FONT_NORMAL
        }

        self.entry_style = {
            "bg": BG_BUTTON,
            "fg": TEXT_NORMAL,
            "font": FONT_NORMAL
        }

        self.list_style = {
            "bg": BG_DARKER,
            "fg": TEXT_NORMAL,
            "font": FONT_NORMAL,
            "selectmode": tk.MULTIPLE
        }

        # Setup main window
        root.title("Git GUI")
        root.config(bg = BG_DARK)
        root.geometry("1200x800")

        # Create toolbar
        toolbar = tk.Frame(root, bg = BG_LIGHTER, height = 35)
        toolbar.pack(side = "top", fill = "x")
        toolbar.pack_propagate(False)

        # Repository selection
        repo_label = tk.Label(toolbar, text = "Repository:", 
                            bg = BG_LIGHTER, 
                            fg = TEXT_NORMAL, 
                            font = FONT_SMALL)
        repo_label.pack(side = "left", padx = 5)

        self.repo_path_var = tk.StringVar(value = self.repo_path)
        self.repo_entry = tk.Entry(toolbar, 
                                 textvariable = self.repo_path_var, 
                                 width = 40, 
                                 **self.entry_style)
        self.repo_entry.pack(side = "left", padx = 5)

        browse_button = tk.Button(toolbar, text = "Browse", command = self.browse_repo, 
                                **self.button_style)
        browse_button.pack(side = "left", padx = 5)

        # Repository URL
        url_label = tk.Label(toolbar, text = "Remote URL:", 
                            bg = BG_LIGHTER, 
                            fg = TEXT_NORMAL, 
                            font = FONT_SMALL)
        url_label.pack(side = "left", padx = 5)

        self.repo_url_var = tk.StringVar(value = self.repo_url)
        self.url_entry = tk.Entry(toolbar, 
                                 textvariable = self.repo_url_var, 
                                 width = 50, 
                                 **self.entry_style)
        self.url_entry.pack(side = "left", padx = 5)

        # Settings button
        settings_button = tk.Button(toolbar, text = "⚙", command = self.show_settings,
                                  **self.button_style)
        settings_button.pack(side = "right", padx = 5)

        # Create main frames
        left_panel = tk.Frame(root, bg = BG_DARK)
        left_panel.pack(side = "left", fill = "both", padx = 10, pady = 10)
        
        center_panel = tk.Frame(root, bg = BG_DARK)
        center_panel.pack(side = "left", fill = "both", expand = True, padx = 10, pady = 10)
        
        # Left side - File lists, buttons and log
        files_frame = tk.Frame(left_panel, bg = BG_DARK)
        files_frame.pack(side = "left", fill = "both", expand = True)  # Changed to expand=True
        
        buttons_frame = tk.Frame(left_panel, bg = BG_DARK)
        buttons_frame.pack(side = "left", fill = "y", padx = (10, 0))

        # Unstaged files section
        unstaged_label = tk.Label(files_frame, text = "Unstaged Changes", 
                                bg = BG_DARK, 
                                fg = TEXT_NORMAL, 
                                font = FONT_TITLE)
        unstaged_label.pack(anchor = "w")

        self.unstaged_file_list = tk.Listbox(files_frame, height = 15, width = 40, **self.list_style)
        self.unstaged_file_list.pack(fill = "x", pady = (0, 10))

        # Staged files section
        staged_label = tk.Label(files_frame, text = "Staged Changes", 
                                bg = BG_DARK, 
                                fg = TEXT_NORMAL, 
                                font = FONT_TITLE)
        staged_label.pack(anchor = "w")

        self.staged_file_list = tk.Listbox(files_frame, height = 15, width = 40, **self.list_style)
        self.staged_file_list.pack(fill = "x", pady = (0, 10))

        # Add log frame under the lists
        log_label = tk.Label(files_frame, text = "Output Log", 
                           bg = BG_DARK, 
                           fg = TEXT_NORMAL, 
                           font = FONT_TITLE)
        log_label.pack(anchor = "w", pady = (10, 5))

        # Create frame for log and its scrollbar
        log_frame = tk.Frame(files_frame, bg = BG_DARK)
        log_frame.pack(fill = "both", expand = True)

        self.log_text = tk.Text(log_frame, height = 10, width = 40, wrap = tk.WORD)
        self.log_text.config(bg = BG_DARKER, fg = TEXT_NORMAL, font = FONT_SMALL)
        self.log_text.pack(side = "left", fill = "both", expand = True)

        # Add log scrollbar
        log_scroll = tk.Scrollbar(log_frame, orient = "vertical", command = self.log_text.yview)
        log_scroll.pack(side = "right", fill = "y")
        self.log_text.configure(yscrollcommand = log_scroll.set)

        # Buttons remain the same in buttons_frame
        self.add_button = tk.Button(buttons_frame, text = "↓ Stage", command = self.add, **self.button_style)
        self.add_button.pack(pady = 5)

        # Unstage button
        self.unstage_button = tk.Button(buttons_frame, text="↑ Unstage", command=self.unstage, **self.button_style)
        self.unstage_button.pack(pady=5)

        # Repository action buttons
        self.pull_button = tk.Button(buttons_frame, text="Pull", command=self.pull, **self.button_style)
        self.pull_button.pack(pady=5)

        self.push_button = tk.Button(buttons_frame, text="Push", command=self.push, **self.button_style)
        self.push_button.pack(pady=5)

        # Center panel - Diff view
        diff_label = tk.Label(center_panel, text="Changes", 
                            bg = BG_DARK, 
                            fg = TEXT_NORMAL, 
                            font = FONT_TITLE)
        diff_label.pack(anchor="w")

        # Add diff text widget with scrollbars
        diff_frame = tk.Frame(center_panel, bg = BG_DARK)
        diff_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.diff_text = tk.Text(diff_frame, wrap=tk.NONE)
        self.diff_text.config(bg = BG_DARKER, fg = TEXT_NORMAL, font = FONT_MONO)
        self.diff_text.pack(side="left", fill="both", expand=True)

        # Vertical scrollbar for diff view
        diff_yscroll = tk.Scrollbar(diff_frame, orient="vertical", command=self.diff_text.yview)
        diff_yscroll.pack(side="right", fill="y")
        self.diff_text.configure(yscrollcommand=diff_yscroll.set)

        # Horizontal scrollbar for diff view
        diff_xscroll = tk.Scrollbar(center_panel, orient="horizontal", command=self.diff_text.xview)
        diff_xscroll.pack(fill="x")
        self.diff_text.configure(xscrollcommand=diff_xscroll.set)

        # Bottom panel - Commit section
        commit_frame = tk.Frame(center_panel, bg = BG_DARK)
        commit_frame.pack(fill="x", side="bottom")

        commit_label = tk.Label(commit_frame, text="Commit Message", 
                                bg = BG_DARK, 
                                fg = TEXT_NORMAL, 
                                font = FONT_TITLE)
        commit_label.pack(side="left")

        self.commit_text_box = tk.Text(commit_frame, height=3, width=50)
        self.commit_text_box.config(bg = BG_DARKER, fg = TEXT_NORMAL, font = FONT_NORMAL)
        self.commit_text_box.pack(side="left", fill="x", expand=True, padx=5)

        self.commit_button = tk.Button(commit_frame, text="Commit", command=self.commit, **self.button_style)
        self.commit_button.pack(side="right")

        # Add bindings for file selection
        self.unstaged_file_list.bind('<<ListboxSelect>>', self.show_unstaged_diff)
        self.staged_file_list.bind('<<ListboxSelect>>', self.show_staged_diff)

    def clone(self):
        git_commands.clone_repo(self.repo_url, self.repo_path)
        self.refresh_lists()

    def add(self):
        selected = self.unstaged_file_list.curselection()
        files_to_stage = [self.unstaged_file_list.get(i) for i in selected]
        success, message = git_commands.add_changes(self.repo_path, files_to_stage)
        self.log_message(message)
        if success:
            self.refresh_lists()

    def unstage(self):
        selected = self.staged_file_list.curselection()
        files_to_unstage = [self.staged_file_list.get(i) for i in selected]
        success, message = git_commands.reset_changes(self.repo_path, files_to_unstage)
        self.log_message(message)
        if success:
            self.refresh_lists()

    def commit(self):
        commit_message = self.commit_text_box.get("1.0", tk.END).strip()
        if commit_message:
            success, message = git_commands.commit_changes(self.repo_path, commit_message)
            self.log_message(message)
            if success:
                self.commit_text_box.delete("1.0", tk.END)
                self.refresh_lists()

    def push(self):
        success, message = git_commands.push_to_repo(self.repo_path)
        self.log_message(message)

    def pull(self):
        success, message = git_commands.pull_from_repo(self.repo_path)
        self.log_message(message)
        if success:
            self.refresh_lists()

    def refresh_lists(self):
        self.unstaged_file_list.delete(0, tk.END)
        self.staged_file_list.delete(0, tk.END)
        self.unstaged_file_list.insert(tk.END, *git_commands.get_unstaged_files(self.repo_path))
        self.staged_file_list.insert(tk.END, *git_commands.get_staged_files(self.repo_path))

    def show_unstaged_diff(self, event=None):
        if self.unstaged_file_list.curselection():
            selected = self.unstaged_file_list.curselection()[0]
            file_path = self.unstaged_file_list.get(selected)
            diff = git_commands.get_file_diff(self.repo_path, file_path, staged=False)
            self.diff_text.delete(1.0, tk.END)
            self.diff_text.insert(tk.END, diff)

    def show_staged_diff(self, event=None):
        if self.staged_file_list.curselection():
            selected = self.staged_file_list.curselection()[0]
            file_path = self.staged_file_list.get(selected)
            diff = git_commands.get_file_diff(self.repo_path, file_path, staged=True)
            self.diff_text.delete(1.0, tk.END)
            self.diff_text.insert(tk.END, diff)

    def browse_repo(self):
        new_path = filedialog.askdirectory(title = "Select Git Repository")
        if new_path:
            try:
                # Verify it's a git repository
                repo = git_commands.Repo(new_path)
                self.repo_path = new_path
                self.repo_path_var.set(new_path)
                self.refresh_lists()
                # Update URL if possible
                try:
                    self.repo_url = repo.remotes.origin.url
                    self.repo_url_var.set(self.repo_url)
                except:
                    pass
            except:
                messagebox.showerror("Error", "Selected directory is not a Git repository")

    def show_settings(self):
        settings_window = tk.Toplevel(bg = BG_DARK)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        # Add settings here
        # Git configuration
        git_frame = tk.LabelFrame(settings_window, text = "Git Configuration", 
                                bg = BG_DARK, 
                                fg = TEXT_NORMAL, 
                                font = FONT_NORMAL)
        git_frame.pack(fill = "x", padx = 10, pady = 5)

        # User name
        name_label = tk.Label(git_frame, text = "User Name:", bg = BG_DARK, fg = TEXT_NORMAL)
        name_label.pack(anchor = "w", padx = 5)
        
        name_entry = tk.Entry(git_frame, bg = BG_BUTTON, fg = TEXT_NORMAL)
        name_entry.insert(0, git_commands.get_config("user.name") or "")
        name_entry.pack(fill = "x", padx = 5)

        # Email
        email_label = tk.Label(git_frame, text = "Email:", bg = BG_DARK, fg = TEXT_NORMAL)
        email_label.pack(anchor = "w", padx = 5)
        
        email_entry = tk.Entry(git_frame, bg = BG_BUTTON, fg = TEXT_NORMAL)
        email_entry.insert(0, git_commands.get_config("user.email") or "")
        email_entry.pack(fill = "x", padx = 5)

        # Save button
        save_button = tk.Button(settings_window, text = "Save", 
                              command = lambda: self.save_settings(name_entry.get(), email_entry.get()),
                              bg = BG_BUTTON, fg = TEXT_NORMAL)
        save_button.pack(pady = 10)

    def save_settings(self, name, email):
        if name:
            git_commands.set_config("user.name", name)
        if email:
            git_commands.set_config("user.email", email)
        messagebox.showinfo("Success", "Settings saved successfully")

    # Add log method
    def log_message(self, message: str):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)  # Auto-scroll to bottom

