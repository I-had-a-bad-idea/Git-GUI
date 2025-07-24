import tkinter as tk
from tkinter import filedialog, messagebox
from git_interface import git_commands

repo_path = "" 
repo_url = ""

class GUIWindow:
    def __init__(self, root) -> None:
        root.title("Git GUI")
        root.config(bg = "gray20")
        root.geometry("1920x1080")

        # Add top toolbar
        toolbar = tk.Frame(root, bg = "gray25", height = 35)
        toolbar.pack(side = "top", fill = "x")
        toolbar.pack_propagate(False)  # Force height

        # Repository selection
        repo_label = tk.Label(toolbar, text = "Repository:", bg = "gray25", fg = "white", font = ("Arial", 10))
        repo_label.pack(side = "left", padx = 5)

        self.repo_path_var = tk.StringVar(value = repo_path)
        self.repo_entry = tk.Entry(toolbar, textvariable = self.repo_path_var, width = 40, bg = "gray30", fg = "white")
        self.repo_entry.pack(side = "left", padx = 5)

        browse_button = tk.Button(toolbar, text = "Browse", command = self.browse_repo, 
                                bg = "gray30", fg = "white", width = 8)
        browse_button.pack(side = "left", padx = 5)

        # Repository URL
        url_label = tk.Label(toolbar, text = "Remote URL:", bg = "gray25", fg = "white", font = ("Arial", 10))
        url_label.pack(side = "left", padx = 5)

        self.repo_url_var = tk.StringVar(value = repo_url)
        self.url_entry = tk.Entry(toolbar, textvariable = self.repo_url_var, width = 50, bg = "gray30", fg = "white")
        self.url_entry.pack(side = "left", padx = 5)

        # Settings button
        settings_button = tk.Button(toolbar, text = "⚙", command = self.show_settings,
                                  bg = "gray30", fg = "white", width = 3)
        settings_button.pack(side = "right", padx = 5)

        # Create main frames
        left_panel = tk.Frame(root, bg = "gray20")
        left_panel.pack(side = "left", fill = "both", padx = 10, pady = 10)
        
        center_panel = tk.Frame(root, bg = "gray20")
        center_panel.pack(side = "left", fill = "both", expand = True, padx = 10, pady = 10)
        
        # Left side - File lists and buttons
        files_frame = tk.Frame(left_panel, bg = "gray20")
        files_frame.pack(side = "left", fill = "y")
        
        buttons_frame = tk.Frame(left_panel, bg = "gray20")
        buttons_frame.pack(side = "left", fill = "y", padx = (10, 0))

        # Unstaged files section
        unstaged_label = tk.Label(files_frame, text = "Unstaged Changes", bg = "gray20", fg = "white", font = ("Arial", 12))
        unstaged_label.pack(anchor = "w")

        self.unstaged_file_list = tk.Listbox(files_frame, height = 15, width = 40, selectmode = tk.MULTIPLE)
        self.unstaged_file_list.insert(tk.END, *git_commands.get_unstaged_files(repo_path))
        self.unstaged_file_list.config(bg = "gray15", fg = "white", font = ("Arial", 11))
        self.unstaged_file_list.pack(fill = "x", pady = (0, 10))

        # Stage button
        button_style = {"width": 12, "font": ("Arial", 11), "bg": "gray30", "fg": "white"}
        self.add_button = tk.Button(buttons_frame, text = "↓ Stage", command = self.add, **button_style)
        self.add_button.pack(pady = 5)

        # Staged files section
        staged_label = tk.Label(files_frame, text = "Staged Changes", bg = "gray20", fg = "white", font = ("Arial", 12))
        staged_label.pack(anchor = "w")

        self.staged_file_list = tk.Listbox(files_frame, height = 15, width = 40, selectmode = tk.MULTIPLE)
        self.staged_file_list.insert(tk.END, *git_commands.get_staged_files(repo_path))
        self.staged_file_list.config(bg = "gray15", fg = "white", font = ("Arial", 11))
        self.staged_file_list.pack(fill = "x")

        # Unstage button
        self.unstage_button = tk.Button(buttons_frame, text="↑ Unstage", command=self.unstage, **button_style)
        self.unstage_button.pack(pady=5)

        # Repository action buttons
        self.pull_button = tk.Button(buttons_frame, text="Pull", command=self.pull, **button_style)
        self.pull_button.pack(pady=5)

        self.push_button = tk.Button(buttons_frame, text="Push", command=self.push, **button_style)
        self.push_button.pack(pady=5)

        # Center panel - Diff view
        diff_label = tk.Label(center_panel, text="Changes", bg="gray20", fg="white", font=("Arial", 12))
        diff_label.pack(anchor="w")

        # Add diff text widget with scrollbars
        diff_frame = tk.Frame(center_panel, bg="gray20")
        diff_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.diff_text = tk.Text(diff_frame, wrap=tk.NONE)
        self.diff_text.config(bg="gray15", fg="white", font=("Courier", 10))
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
        commit_frame = tk.Frame(center_panel, bg="gray20")
        commit_frame.pack(fill="x", side="bottom")

        commit_label = tk.Label(commit_frame, text="Commit Message", bg="gray20", fg="white", font=("Arial", 12))
        commit_label.pack(side="left")

        self.commit_text_box = tk.Text(commit_frame, height=3, width=50)
        self.commit_text_box.config(bg="gray15", fg="white", font=("Arial", 11))
        self.commit_text_box.pack(side="left", fill="x", expand=True, padx=5)

        self.commit_button = tk.Button(commit_frame, text="Commit", command=self.commit, **button_style)
        self.commit_button.pack(side="right")

        # Add bindings for file selection
        self.unstaged_file_list.bind('<<ListboxSelect>>', self.show_unstaged_diff)
        self.staged_file_list.bind('<<ListboxSelect>>', self.show_staged_diff)

    def clone(self):
        git_commands.clone_repo(repo_url, repo_path)
        self.refresh_lists()

    def add(self):
        selected = self.unstaged_file_list.curselection()
        files_to_stage = [self.unstaged_file_list.get(i) for i in selected]
        git_commands.add_changes(repo_path, files_to_stage)
        self.refresh_lists()

    def unstage(self):
        selected = self.staged_file_list.curselection()
        files_to_unstage = [self.staged_file_list.get(i) for i in selected]
        git_commands.reset_changes(repo_path, files_to_unstage)  # You'll need to add this method to git_commands
        self.refresh_lists()

    def commit(self):
        commit_message = self.commit_text_box.get("1.0", tk.END).strip()
        if commit_message:
            git_commands.commit_changes(repo_path, commit_message)
            self.commit_text_box.delete("1.0", tk.END)
            self.refresh_lists()

    def push(self):
        git_commands.push_to_repo(repo_path)

    def pull(self):
        git_commands.pull_from_repo(repo_path)
        self.refresh_lists()

    def refresh_lists(self):
        self.unstaged_file_list.delete(0, tk.END)
        self.staged_file_list.delete(0, tk.END)
        self.unstaged_file_list.insert(tk.END, *git_commands.get_unstaged_files(repo_path))
        self.staged_file_list.insert(tk.END, *git_commands.get_staged_files(repo_path))

    def show_unstaged_diff(self, event=None):
        if self.unstaged_file_list.curselection():
            selected = self.unstaged_file_list.curselection()[0]
            file_path = self.unstaged_file_list.get(selected)
            diff = git_commands.get_file_diff(repo_path, file_path, staged=False)
            self.diff_text.delete(1.0, tk.END)
            self.diff_text.insert(tk.END, diff)

    def show_staged_diff(self, event=None):
        if self.staged_file_list.curselection():
            selected = self.staged_file_list.curselection()[0]
            file_path = self.staged_file_list.get(selected)
            diff = git_commands.get_file_diff(repo_path, file_path, staged=True)
            self.diff_text.delete(1.0, tk.END)
            self.diff_text.insert(tk.END, diff)

    def browse_repo(self):
        new_path = filedialog.askdirectory(title = "Select Git Repository")
        if new_path:
            try:
                # Verify it's a git repository
                repo = git_commands.Repo(new_path)
                self.repo_path_var.set(new_path)
                global repo_path
                repo_path = new_path
                self.refresh_lists()
                # Update URL if possible
                try:
                    remote_url = repo.remotes.origin.url
                    self.repo_url_var.set(remote_url)
                    global repo_url
                    repo_url = remote_url
                except:
                    pass
            except:
                messagebox.showerror("Error", "Selected directory is not a Git repository")

    def show_settings(self):
        settings_window = tk.Toplevel(bg = "gray20")
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        # Add settings here
        # Git configuration
        git_frame = tk.LabelFrame(settings_window, text = "Git Configuration", 
                                bg = "gray20", fg = "white", font = ("Arial", 11))
        git_frame.pack(fill = "x", padx = 10, pady = 5)

        # User name
        name_label = tk.Label(git_frame, text = "User Name:", bg = "gray20", fg = "white")
        name_label.pack(anchor = "w", padx = 5)
        
        name_entry = tk.Entry(git_frame, bg = "gray30", fg = "white")
        name_entry.insert(0, git_commands.get_config("user.name") or "")
        name_entry.pack(fill = "x", padx = 5)

        # Email
        email_label = tk.Label(git_frame, text = "Email:", bg = "gray20", fg = "white")
        email_label.pack(anchor = "w", padx = 5)
        
        email_entry = tk.Entry(git_frame, bg = "gray30", fg = "white")
        email_entry.insert(0, git_commands.get_config("user.email") or "")
        email_entry.pack(fill = "x", padx = 5)

        # Save button
        save_button = tk.Button(settings_window, text = "Save", 
                              command = lambda: self.save_settings(name_entry.get(), email_entry.get()),
                              bg = "gray30", fg = "white")
        save_button.pack(pady = 10)

    def save_settings(self, name, email):
        if name:
            git_commands.set_config("user.name", name)
        if email:
            git_commands.set_config("user.email", email)
        messagebox.showinfo("Success", "Settings saved successfully")

