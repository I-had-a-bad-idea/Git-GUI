import tkinter as tk
from tkinter import ttk, messagebox
from git_interface import git_commands
from .theme import *

#TODO currently removed, should this even be reimplemented?

class GraphWindow:
    def __init__(self, root, repo_path):
        self.window = tk.Toplevel(root)
        self.window.title("Git History")
        self.window.geometry("800x600")
        self.window.config(bg = BG_DARK)
        
        self.repo_path = repo_path
        
        # Create main canvas for the graph
        self.canvas_frame = tk.Frame(self.window, bg = BG_DARK)
        self.canvas_frame.pack(fill = "both", expand = True, padx = 10, pady = 10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg = BG_DARKER)
        self.canvas.pack(side = "left", fill = "both", expand = True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Draw the graph
        self.draw_graph()
        
        # Add refresh button
        refresh_button = tk.Button(self.window, text = "Refresh", 
                                 command=self.refresh_graph,
                                 **BUTTON_STYLE)
        refresh_button.pack(pady=5)

    def draw_graph(self):
        self.canvas.delete("all")  # Clear existing content
        
        # Get git log with graph info
        success, message, branches = git_commands.get_branches(self.repo_path)
        if not success:
            messagebox.showerror("Error", message)
            return
        
        branches = branches["branches"]

            
        # Start coordinates
        x_start = 50
        y_start = 50
        y_spacing = 40
        branch_spacing = 20
        print(f"Branches: {branches}")

        commits_in_branches : dict = {}

        for branch in branches:
            commits_in_branches[branch] = git_commands.get_commits_in_branch(self.repo_path, branch)[2]

        print(f"Commits in branches: {commits_in_branches}")

        commits : list = []

        for branch in branches:
            for commit in commits_in_branches[branch]:
                if commit in commits:
                    continue
                commits.append([commit, branch])

        commits.sort(key = lambda x: x[0].committed_datetime, reverse = True)
        
        print(f"Commits: {commits}")

        drawn_commits : list = []

        for commit_data in commits:
            commit, branch = commit_data
            if commit in drawn_commits:
                continue
            x = x_start + branches.index(branch) * branch_spacing
            y = y_start + len(drawn_commits) * y_spacing

            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                  fill = BG_LIGHTER, outline = TEXT_NORMAL)
                
            commit_text = f"{commit.message})"
            self.canvas.create_text(x + 20, y, anchor="w",
                                  text = commit_text, fill = TEXT_NORMAL,
                                  font = FONT_NORMAL)
                
            self.canvas.create_line(x, y + 5, x, y + y_spacing - 5,
                                 fill = TEXT_NORMAL)
                
            drawn_commits.append(commit)

        total_height = len(drawn_commits) * y_spacing + y_start * 2
        self.canvas.configure(scrollregion = (0, 0, 800, total_height))
               

    def refresh_graph(self):
        self.draw_graph()
