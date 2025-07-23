import tkinter as tk
from git_interface import git_commands

repo_path = "E:/Git-GUI"  #TODO Make this configurable

repo_url = "https://github.com/I-had-a-bad-idea/Git-GUI.git" #TODO Make this configurable

class GUIWindow:

    def __init__(self, root) -> None:
        root.title("Git GUI")

        root.config(bg = "black")
        
        clone_button = tk.Button(root, text = "Clone", command = clone)
        clone_button.pack(pady = 10)

        add_button = tk.Button(root, text = "Add", command = add)
        add_button.pack(pady = 10)

        commit_button = tk.Button(root, text = "Commit", command = commit)
        commit_button.pack(pady = 10)

        pull_button = tk.Button(root, text = "Pull", command = pull)
        pull_button.pack(pady = 10)

        push_button = tk.Button(root, text = "Push", command = push)
        push_button.pack(pady = 10)

        commit_text_box = tk.Text(root, height = 5, width = 50)
        commit_text_box.config(bg = "dark gray", fg = "black", font = ("Arial", 12))
        commit_text_box.pack(pady = 10)

        unstaged_file_list = tk.Listbox(root, height = 10, width = 50)
        unstaged_file_list.insert(tk.END, *git_commands.get_unstaged_files(repo_path))
        unstaged_file_list.config(bg = "black", fg = "gray", font = ("Arial", 12))
        unstaged_file_list.pack(pady = 10)

        staged_file_list = tk.Listbox(root, height = 10, width = 50)
        staged_file_list.insert(tk.END, *git_commands.get_staged_files(repo_path))
        staged_file_list.config(bg = "black", fg = "gray", font = ("Arial", 12))
        staged_file_list.pack(pady = 10)

def clone():
    git_commands.clone_repo(repo_url, repo_path)

def add():
    git_commands.add_changes(repo_path, git_commands.get_unstaged_files(repo_path))  # TODO Make this not always use all files

def commit():
    git_commands.commit_changes(repo_path, "This commit was made with the GUI (kinda)")  # TODO Make this use an actual message

def push():
    git_commands.push_to_repo(repo_path)

def pull():
    git_commands.pull_from_repo(repo_path)

