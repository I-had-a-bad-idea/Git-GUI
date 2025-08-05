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
        branch_spacing = 60  # Increased spacing for better visibility

        furthest_x = len(branches) * branch_spacing + x_start


        commits_in_branches : dict = {}

        for branch in branches:
            commits_in_branches[branch] = git_commands.get_commits_in_branch(self.repo_path, branch)[2]


        # Create a mapping of commits to their positions and branch info
        commit_positions = {}  # commit_hash -> (x, y, branch)
        commits : list = []

        for branch in branches:
            for commit in commits_in_branches[branch]:
                if commit in commits:
                    continue
                commits.append([commit, branch])

        commits.sort(key = lambda x: x[0].committed_datetime, reverse = True)
        
        drawn_commits : list = []

        # First pass: draw commits and store their positions
        for i, commit_data in enumerate(commits):
            commit, branch = commit_data
            if commit in drawn_commits:
                continue
            
            x = x_start + branches.index(branch) * branch_spacing
            y = y_start + len(drawn_commits) * y_spacing

            # Store position for line drawing
            commit_positions[commit.hexsha] = (x, y, branch)

            # Draw commit circle and text
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                  fill = BG_LIGHTER, outline = TEXT_NORMAL)
                
            commit_text = f"{commit.message}"
            self.canvas.create_text(furthest_x - 20, y, anchor="w",
                                  text = commit_text, fill = TEXT_NORMAL,
                                  font = FONT_NORMAL)
                
            drawn_commits.append(commit)

        # Second pass: draw connecting lines between commits and their parents

        for commit_data in commits:
            commit, branch = commit_data
            if commit.hexsha not in commit_positions:
                continue
                
            current_x, current_y, current_branch = commit_positions[commit.hexsha]
            
            # Draw lines to parent commits
            for parent in commit.parents:
                parent_hash = parent.hexsha
                if parent_hash in commit_positions:
                    parent_x, parent_y, parent_branch = commit_positions[parent_hash]
                    
                    # Choose line color based on whether it's the same branch
                    line_color = TEXT_NORMAL if current_branch == parent_branch else TEXT_GRAY
                    
                    if current_x == parent_x:
                        # Straight line for same branch
                        self.canvas.create_line(current_x, current_y + 5, 
                                              parent_x, parent_y - 5,
                                              fill = line_color, width = 2)
                    else:
                        # Curved line for merges/branches - simplified as angled line
                        # Draw line from current commit down, then across, then up to parent
                        mid_y = current_y + (parent_y - current_y) / 2
                        
                        self.canvas.create_line(current_x, current_y + 5,
                                              current_x, mid_y,
                                              fill = line_color, width = 2)
                        self.canvas.create_line(current_x, mid_y,
                                              parent_x, mid_y,
                                              fill = line_color, width = 2)
                        self.canvas.create_line(parent_x, mid_y,
                                              parent_x, parent_y - 5,
                                              fill = line_color, width = 2)

        # Draw branch lanes (vertical lines showing branch continuity)
        for i, branch in enumerate(branches):
            x = x_start + i * branch_spacing
            branch_commits = [pos for hash, pos in commit_positions.items() 
                            if pos[2] == branch]
            
            if len(branch_commits) > 1:
                branch_commits.sort(key=lambda pos: pos[1])  # Sort by y position
                start_y = branch_commits[0][1]
                
                # Add branch label at the top
                self.canvas.create_text(x, start_y - 20, anchor="center",
                                      text = branch, fill = TEXT_NORMAL,
                                      font = ("Arial", 8))

        total_height = len(drawn_commits) * y_spacing + y_start * 2
        self.canvas.configure(scrollregion = (0, 0, 800, total_height))
               

    def refresh_graph(self):
        self.draw_graph()