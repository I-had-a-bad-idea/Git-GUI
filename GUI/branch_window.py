import tkinter as tk
from tkinter import messagebox
from git_interface import git_commands
from .theme import *

class BranchWindow:
    def __init__(self, root, repo_path, refresh_callback):
        self.window = tk.Toplevel(root)
        self.window.title("Branch Management")
        self.window.geometry("400x500")
        self.window.config(bg = BG_DARK)
        
        self.repo_path = repo_path
        self.refresh_callback = refresh_callback
        
        # Branch list
        list_frame = tk.Frame(self.window, bg = BG_DARK)
        list_frame.pack(fill = "both", expand = True, padx = 10, pady = 5)
        
        list_label = tk.Label(list_frame, text = "Branches", **LABEL_STYLE)
        list_label.pack(anchor = "w")
        
        self.branch_list = tk.Listbox(list_frame, **LIST_STYLE)
        self.branch_list.pack(fill = "both", expand = True)
        
        # New branch frame
        new_branch_frame = tk.Frame(self.window, bg = BG_DARK)
        new_branch_frame.pack(fill = "x", padx=10, pady = 5)
        
        self.new_branch_entry = tk.Entry(new_branch_frame, **ENTRY_STYLE)
        self.new_branch_entry.pack(side = "left", expand = True, fill = "x", padx = (0, 5))
        
        create_button = tk.Button(new_branch_frame, text = "Create Branch",
                                command = self.create_branch, **BUTTON_STYLE)
        create_button.pack(side = "right")
        
        # Action buttons
        button_frame = tk.Frame(self.window, bg = BG_DARK)
        button_frame.pack(fill = "x", padx = 10, pady = 5)
        
        switch_button = tk.Button(button_frame, text = "Switch to Branch",
                                command = self.switch_branch, **BUTTON_STYLE)
        switch_button.pack(side = "left", padx = 5)
        
        delete_button = tk.Button(button_frame, text = "Delete Branch",
                                command = self.delete_branch, **BUTTON_STYLE)
        delete_button.pack(side="right", padx=5)
        
        self.refresh_branches()
    
    def refresh_branches(self):
        success, message, data = git_commands.get_branches(self.repo_path)
        if success:
            self.branch_list.delete(0, tk.END)
            for branch in data["branches"]:
                text = f"* {branch}" if branch == data["current"] else f"  {branch}"
                self.branch_list.insert(tk.END, text)
        else:
            messagebox.showerror("Error", message)
    
    def create_branch(self):
        branch_name = self.new_branch_entry.get().strip()
        if branch_name:
            success, message = git_commands.create_branch(self.repo_path, branch_name)
            if success:
                self.new_branch_entry.delete(0, tk.END)
                self.refresh_branches()
                self.refresh_callback()
            messagebox.showinfo("Branch Creation", message)
    
    def delete_branch(self):
        selection = self.branch_list.curselection()
        if selection:
            branch_name = self.branch_list.get(selection[0]).strip()
            if branch_name.startswith("* "):
                messagebox.showerror("Error", "Cannot delete current branch")
                return
            success, message = git_commands.delete_branch(self.repo_path, branch_name)
            if success:
                self.refresh_branches()
            messagebox.showinfo("Deleted", message)
    
    def switch_branch(self):
        selection = self.branch_list.curselection()
        if selection:
            branch_name = self.branch_list.get(selection[0]).strip()
            if branch_name.startswith("* "):
                messagebox.showinfo("Info", "Already on this branch")
                return
            success, message = git_commands.switch_branch(self.repo_path, branch_name)
            if success:
                self.refresh_branches()
                self.refresh_callback()
            messagebox.showinfo("Swiched branch to", message)