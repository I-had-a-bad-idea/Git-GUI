import tkinter as tk
from git_interface import git_commands

repo_path = "E:/Git-GUI"  #TODO Make this configurable


class GUIWindow:

    def __init__(self, root) -> None:
        root.title("Git GUI")

        root.config(bg = "black")
        
        add_button = tk.Button(root, text = "Add", command = add)
        add_button.pack(pady = 10)

        commit_button = tk.Button(root, text = "Commit", command = commit)
        commit_button.pack(pady = 10)

        pull_button = tk.Button(root, text = "Pull", command = pull)
        pull_button.pack(pady = 10)

        push_button = tk.Button(root, text = "Push", command = push)
        push_button.pack(pady = 10)

        commit_text_box = tk.Text(root, height = 5, width = 50)
        commit_text_box.config(bg = "dark gray", fg = "black", font=("Arial", 12))
        commit_text_box.pack(pady = 10)


def add():
    git_commands.add_changes(repo_path, git_commands.get_unstaged_files(repo_path))  # TODO Make this not always use all files

def commit():
    git_commands.commit_changes(repo_path, "This commit was made with the GUI (kinda)")  # TODO Make this use an actual message

def push():
    git_commands.push_to_repo(repo_path)

def pull():
    git_commands.pull_from_repo(repo_path)