import tkinter as tk
from tkinter import ttk
from git_interface import git_commands
from .theme import *

#TODO currently removed, should this even be reimplemented?

class GraphWindow:
    def __init__(self, root, repo_path):
        self.window = tk.Toplevel(root)
        self.window.title("Git History")
        self.window.geometry("800x600")
        self.window.config(bg=BG_DARK)
        
        self.repo_path = repo_path
        
        # Create main canvas for the graph
        self.canvas_frame = tk.Frame(self.window, bg=BG_DARK)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg=BG_DARKER)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Draw the graph
        self.draw_graph()
        
        # Add refresh button
        refresh_button = tk.Button(self.window, text="Refresh", 
                                 command=self.refresh_graph,
                                 **BUTTON_STYLE)
        refresh_button.pack(pady=5)

    def draw_graph(self):
        self.canvas.delete("all")  # Clear existing content
        
        # Get git log with graph info
        success, message, commits = git_commands.get_log(self.repo_path)
        if not success:
            self.canvas.create_text(10, 10, anchor="nw", text=message, 
                                  fill=TEXT_NORMAL, font=FONT_NORMAL)
            return
            
        # Start coordinates
        x_start = 50
        y_start = 50
        y_spacing = 40
        branch_spacing = 20
        
        # Draw commits
        for i, commit in enumerate(commits):
            y = y_start + (i * y_spacing)
            
            # Draw commit circle
            self.canvas.create_oval(x_start-5, y-5, x_start+5, y+5, 
                                  fill=BG_LIGHTER, outline=TEXT_NORMAL)
            
            # Draw commit info
            commit_text = f"{commit['commit'][:7]} - {commit['message']} ({commit['author']})"
            self.canvas.create_text(x_start + 20, y, anchor="w", 
                                  text=commit_text, fill=TEXT_NORMAL, 
                                  font=FONT_NORMAL)
            
            # Draw lines to parent commits
            if i < len(commits) - 1:
                self.canvas.create_line(x_start, y+5, x_start, y+y_spacing-5, 
                                     fill=TEXT_NORMAL)
        
        # Update canvas scroll region
        total_height = len(commits) * y_spacing + y_start * 2
        self.canvas.configure(scrollregion=(0, 0, 800, total_height))

    def refresh_graph(self):
        self.draw_graph()
